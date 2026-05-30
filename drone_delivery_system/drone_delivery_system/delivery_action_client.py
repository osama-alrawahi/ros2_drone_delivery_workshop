#!/usr/bin/env python3
"""
delivery_action_client.py
=========================
WORKSHOP PART 7 — ACTIONS

Sends a delivery mission and monitors live progress.

Usage:
  ros2 run drone_delivery_system delivery_action_client

Or via CLI (no Python client needed):
  ros2 action send_goal /deliver_package \
    drone_delivery_interfaces/action/DeliverPackage \
    "{package_id: 'PKG-001', destination_name: 'SQU', \
      target_latitude: 23.6097, target_longitude: 58.1804, max_speed: 15.0}" \
    --feedback
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from drone_delivery_interfaces.action import DeliverPackage


class DeliveryActionClient(Node):
    """Sends a delivery goal and streams live progress to the terminal."""

    def __init__(self):
        super().__init__('delivery_action_client')

        # ── Action Client ─────────────────────────────────────────────────────
        # Must match the server's action type and name exactly
        self._client = ActionClient(self, DeliverPackage, '/deliver_package')

    def send_mission(self, package_id, destination_name, latitude, longitude, speed=15.0):
        """Send goal to the action server asynchronously."""
        self.get_logger().info('⏳ Waiting for /deliver_package action server...')
        self._client.wait_for_server()   # Block until server is up

        # Build the goal
        goal                     = DeliverPackage.Goal()
        goal.package_id          = package_id
        goal.destination_name    = destination_name
        goal.target_latitude     = latitude
        goal.target_longitude    = longitude
        goal.max_speed           = speed

        self.get_logger().info('=' * 55)
        self.get_logger().info(f'  🚀 SENDING DELIVERY MISSION')
        self.get_logger().info(f'  Package : {package_id}')
        self.get_logger().info(f'  To      : {destination_name}')
        self.get_logger().info(f'  Coords  : ({latitude:.4f}°N, {longitude:.4f}°E)')
        self.get_logger().info(f'  Speed   : {speed} m/s')
        self.get_logger().info('=' * 55)

        # send_goal_async returns immediately with a Future
        # feedback_callback fires every time the server publishes feedback
        future = self._client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        future.add_done_callback(self.goal_response_callback)

    # ── Callback 1: Goal accepted / rejected ──────────────────────────────────
    def goal_response_callback(self, future):
        """Called once the server responds to our goal submission."""
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('❌ Mission REJECTED by server!')
            rclpy.shutdown()
            return

        self.get_logger().info('✅ Mission ACCEPTED — delivery in progress…')
        self.get_logger().info('─' * 55)

        # Register callback for the final result
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    # ── Callback 2: Live feedback ─────────────────────────────────────────────
    def feedback_callback(self, feedback_msg):
        """Called every time the server publishes a feedback update."""
        fb = feedback_msg.feedback

        # Build a progress bar
        bar_len = 25
        filled  = int(fb.progress_percent / 100 * bar_len)
        bar     = f'[{"█" * filled}{"░" * (bar_len - filled)}]'

        phase_emoji = {
            'TAKEOFF':               '🚀',
            'FLYING_TO_DESTINATION': '✈️ ',
            'DELIVERING_PACKAGE':    '📦',
            'RETURNING_HOME':        '🔄',
            'LANDING':               '🛬',
        }.get(fb.current_phase, '❓')

        self.get_logger().info(
            f'{phase_emoji} {bar} {fb.progress_percent:5.1f}% | '
            f'🔋{fb.battery_remaining:.0f}% | '
            f'⏱️ {fb.estimated_time_remaining:.0f}s | '
            f'{fb.status_message}'
        )

    # ── Callback 3: Final result ──────────────────────────────────────────────
    def result_callback(self, future):
        """Called when the mission ends (success, cancel, or abort)."""
        result = future.result().result
        self.get_logger().info('─' * 55)

        if result.success:
            self.get_logger().info('🏆 DELIVERY COMPLETE!')
            self.get_logger().info(f'  {result.message}')
            self.get_logger().info(f'  Distance : {result.total_distance_km:.2f} km')
            self.get_logger().info(f'  Time     : {result.delivery_time_seconds:.1f} s')
        else:
            self.get_logger().error(f'❌ Mission ended: {result.message}')

        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    client = DeliveryActionClient()

    # Send mission to Sultan Qaboos University
    client.send_mission(
        package_id='PKG-2024-001',
        destination_name='Sultan Qaboos University',
        latitude=23.6097,
        longitude=58.1804,
        speed=15.0,
    )

    rclpy.spin(client)   # keep running to receive callbacks


if __name__ == '__main__':
    main()
