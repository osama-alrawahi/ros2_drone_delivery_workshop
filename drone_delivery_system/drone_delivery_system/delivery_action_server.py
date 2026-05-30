#!/usr/bin/env python3
"""
delivery_action_server.py
=========================
WORKSHOP PART 7 — ACTIONS

Manages complete drone delivery missions end-to-end.

Mission phases and progress mapping:
  Phase 1  TAKEOFF             (  0% → 10%)
  Phase 2  FLY_TO_DESTINATION  ( 10% → 50%)
  Phase 3  DELIVERING_PACKAGE  ( 50% → 70%)
  Phase 4  RETURNING_HOME      ( 70% → 95%)
  Phase 5  LANDING             ( 95% →100%)

Action:
  /deliver_package  (drone_delivery_interfaces/DeliverPackage)

Run:
  ros2 run drone_delivery_system delivery_action_server

Test with CLI:
  ros2 action send_goal /deliver_package \
    drone_delivery_interfaces/action/DeliverPackage \
    "{package_id: 'PKG-001', destination_name: 'SQU', \
      target_latitude: 23.6097, target_longitude: 58.1804, max_speed: 15.0}" \
    --feedback

Or run the Python client:
  ros2 run drone_delivery_system delivery_action_client

Cancel mid-mission (run in another terminal):
  ros2 action cancel /deliver_package <goal_id>
"""

import math
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
from drone_delivery_interfaces.action import DeliverPackage


class DeliveryActionServer(Node):
    """Action server for complete autonomous drone delivery missions."""

    def __init__(self):
        super().__init__('delivery_action_server')

        # Home base — Muscat, Oman
        self.home_lat = 23.5880
        self.home_lon = 58.3829

        # ── Parameters ────────────────────────────────────────────────────────
        self.declare_parameter('drone_speed_ms',       15.0)
        self.declare_parameter('max_altitude',         120.0)
        self.declare_parameter('delivery_hover_time',  10.0)

        self.drone_speed = (
            self.get_parameter('drone_speed_ms')
            .get_parameter_value().double_value
        )

        # ReentrantCallbackGroup lets cancel callbacks run
        # while the execute callback is blocking (needed for cancellation)
        self._cb_group = ReentrantCallbackGroup()

        # ── Action Server ─────────────────────────────────────────────────────
        self._action_server = ActionServer(
            self,
            DeliverPackage,
            '/deliver_package',
            execute_callback=self.execute_callback,   # ← main mission logic
            goal_callback=self.goal_callback,          # ← accept or reject goal
            cancel_callback=self.cancel_callback,      # ← accept or reject cancel
            callback_group=self._cb_group,
        )

        # Publish state changes
        self.state_pub = self.create_publisher(String, '/drone_state_command', 10)

        self.get_logger().info('=' * 50)
        self.get_logger().info('  Delivery Action Server — READY')
        self.get_logger().info('  Action: /deliver_package')
        self.get_logger().info(f'  Speed : {self.drone_speed} m/s')
        self.get_logger().info('  Waiting for delivery goals...')
        self.get_logger().info('=' * 50)

    # ── Goal callback ──────────────────────────────────────────────────────────
    def goal_callback(self, goal_request):
        """
        Called BEFORE accepting a goal — decide accept/reject.
        Add validation here (check battery, airspace, payload weight, etc.)
        """
        self.get_logger().info(
            f'📦 New goal: {goal_request.package_id} → {goal_request.destination_name}'
        )
        return GoalResponse.ACCEPT   # Accept all goals for workshop demo

    # ── Cancel callback ────────────────────────────────────────────────────────
    def cancel_callback(self, goal_handle):
        """Called when client requests cancellation mid-mission."""
        self.get_logger().warn('⚠️  Cancel requested!')
        return CancelResponse.ACCEPT  # Accept all cancellations

    # ── Execute callback ───────────────────────────────────────────────────────
    def execute_callback(self, goal_handle):
        """
        Main mission logic — runs the entire delivery from takeoff to landing.
        Runs in a separate thread (thanks to MultiThreadedExecutor).

        key goal_handle methods:
          goal_handle.request              — original goal data
          goal_handle.is_cancel_requested  — True if cancel was called
          goal_handle.publish_feedback(fb) — send progress to client
          goal_handle.succeed()            — mark mission as succeeded
          goal_handle.canceled()           — mark mission as canceled
          goal_handle.abort()              — mark mission as failed
        """
        g = goal_handle.request
        self.get_logger().info(f'🚀 Mission started: {g.package_id} → {g.destination_name}')

        distance_km  = self._haversine(self.home_lat, self.home_lon, g.target_latitude, g.target_longitude)
        mission_start = time.time()
        battery       = 100.0
        fb            = DeliverPackage.Feedback()   # reuse this object

        # ── Helper: check cancel and publish feedback ──────────────────────────
        def tick(phase, progress, status, lat, lon, eta):
            """Publish one feedback update. Returns True if should abort."""
            if goal_handle.is_cancel_requested:
                return True
            nonlocal battery
            battery = max(0.0, 100.0 - (time.time() - mission_start) * 0.1
                          - distance_km * 3.0 * (progress / 100.0))
            fb.progress_percent        = progress
            fb.current_phase           = phase
            fb.status_message          = status
            fb.current_latitude        = lat
            fb.current_longitude       = lon
            fb.battery_remaining       = battery
            fb.estimated_time_remaining = eta
            goal_handle.publish_feedback(fb)
            return False

        # ─────────────────────────────────────────────────────────────────────
        # PHASE 1 — TAKEOFF (0 → 10%)
        # ─────────────────────────────────────────────────────────────────────
        self._pub_state('TAKING_OFF')
        self.get_logger().info('📍 Phase 1: TAKEOFF')

        for step in range(11):
            if tick('TAKEOFF', float(step),
                    f'Ascending… {step * 5}m / 50m',
                    self.home_lat, self.home_lon,
                    float(distance_km * 2 * 1000 / self.drone_speed)):
                goal_handle.canceled()
                return self._result(False, 'Cancelled during takeoff')
            time.sleep(0.3)

        # ─────────────────────────────────────────────────────────────────────
        # PHASE 2 — FLY TO DESTINATION (10 → 50%)
        # ─────────────────────────────────────────────────────────────────────
        self._pub_state('FLYING')
        self.get_logger().info(f'📍 Phase 2: FLYING ({distance_km:.2f} km)')

        steps = 40
        for step in range(steps + 1):
            r = step / steps
            lat = self.home_lat + (g.target_latitude  - self.home_lat) * r
            lon = self.home_lon + (g.target_longitude - self.home_lon) * r
            eta = distance_km * (1 - r) * 1000 / self.drone_speed

            if tick('FLYING_TO_DESTINATION',
                    10.0 + r * 40.0,
                    f'En route — {distance_km * (1 - r):.1f} km remaining',
                    lat, lon, eta):
                goal_handle.canceled()
                return self._result(False, 'Cancelled during flight')

            if step % 10 == 0:
                self.get_logger().info(
                    f'  ✈️  {10 + r*40:.0f}% | ETA: {eta:.0f}s'
                )
            time.sleep(0.2)

        # ─────────────────────────────────────────────────────────────────────
        # PHASE 3 — DELIVERING PACKAGE (50 → 70%)
        # ─────────────────────────────────────────────────────────────────────
        self._pub_state('DELIVERING')
        self.get_logger().info('📍 Phase 3: DELIVERING PACKAGE')

        descs = ['Hovering…', 'Lowering package…', 'Package released ✓']
        for step in range(21):
            desc = descs[min(step // 7, 2)]
            if tick('DELIVERING_PACKAGE',
                    50.0 + step,
                    f'📦 {desc} [{g.package_id}]',
                    g.target_latitude, g.target_longitude,
                    float(distance_km * 1000 / self.drone_speed)):
                goal_handle.canceled()
                return self._result(False, 'Cancelled during delivery')
            if step % 5 == 0:
                self.get_logger().info(f'  📦 {50 + step:.0f}% | {desc}')
            time.sleep(0.25)

        self.get_logger().info(f'  ✅ Package {g.package_id} delivered!')

        # ─────────────────────────────────────────────────────────────────────
        # PHASE 4 — RETURN HOME (70 → 95%)
        # ─────────────────────────────────────────────────────────────────────
        self._pub_state('RETURNING')
        self.get_logger().info('📍 Phase 4: RETURNING HOME')

        steps = 25
        for step in range(steps + 1):
            r = step / steps
            lat = g.target_latitude  + (self.home_lat - g.target_latitude)  * r
            lon = g.target_longitude + (self.home_lon - g.target_longitude) * r
            eta = distance_km * (1 - r) * 1000 / self.drone_speed

            if tick('RETURNING_HOME',
                    70.0 + r * 25.0,
                    f'Returning — {distance_km * (1 - r):.1f} km remaining',
                    lat, lon, eta):
                goal_handle.canceled()
                return self._result(False, 'Cancelled during return')

            if step % 8 == 0:
                self.get_logger().info(f'  🔄 {70 + r*25:.0f}% | ETA: {eta:.0f}s')
            time.sleep(0.2)

        # ─────────────────────────────────────────────────────────────────────
        # PHASE 5 — LANDING (95 → 100%)
        # ─────────────────────────────────────────────────────────────────────
        self._pub_state('LANDING')
        self.get_logger().info('📍 Phase 5: LANDING')

        for step in range(6):
            if tick('LANDING',
                    95.0 + step,
                    f'Descending… {(5 - step) * 10}m above ground',
                    self.home_lat, self.home_lon, float(5 - step)):
                goal_handle.canceled()
                return self._result(False, 'Cancelled during landing')
            self.get_logger().info(f'  ↓ {(5 - step) * 10}m')
            time.sleep(0.4)

        # ─────────────────────────────────────────────────────────────────────
        # MISSION COMPLETE
        # ─────────────────────────────────────────────────────────────────────
        self._pub_state('IDLE')

        total_time = time.time() - mission_start
        total_dist = distance_km * 2  # round trip

        goal_handle.succeed()

        result                        = DeliverPackage.Result()
        result.success                = True
        result.message                = f'✅ MISSION COMPLETE — {g.package_id} delivered to {g.destination_name}'
        result.delivery_time_seconds  = total_time
        result.total_distance_km      = total_dist

        self.get_logger().info('=' * 50)
        self.get_logger().info('  🏆 MISSION COMPLETE')
        self.get_logger().info(f'  Package  : {g.package_id}')
        self.get_logger().info(f'  Location : {g.destination_name}')
        self.get_logger().info(f'  Time     : {total_time:.1f} s')
        self.get_logger().info(f'  Distance : {total_dist:.2f} km')
        self.get_logger().info('=' * 50)
        return result

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _pub_state(self, state):
        msg      = String()
        msg.data = state
        self.state_pub.publish(msg)

    def _result(self, success, message):
        r                       = DeliverPackage.Result()
        r.success               = success
        r.message               = message
        r.delivery_time_seconds = 0.0
        r.total_distance_km     = 0.0
        return r

    def _haversine(self, lat1, lon1, lat2, lon2):
        """Great-circle distance in km using the Haversine formula."""
        R    = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a    = (math.sin(dlat / 2) ** 2
                + math.cos(math.radians(lat1))
                * math.cos(math.radians(lat2))
                * math.sin(dlon / 2) ** 2)
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def main(args=None):
    rclpy.init(args=args)
    node = DeliveryActionServer()

    # MultiThreadedExecutor is required so the cancel callback can run
    # while execute_callback is blocking inside the mission loop
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info('Delivery Action Server shutting down...')
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
