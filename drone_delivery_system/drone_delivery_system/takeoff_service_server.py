#!/usr/bin/env python3
"""
takeoff_service_server.py
=========================
WORKSHOP PART 6 — SERVICES

Provides two services:
  /takeoff  (std_srvs/Trigger) — Command drone to take off
  /land     (std_srvs/Trigger) — Command drone to land

std_srvs/Trigger is a built-in service:
  Request:  (empty — just calling it is the request)
  Response: bool    success
            string  message

Run server:
  ros2 run drone_delivery_system takeoff_service_server

Test with the CLI (no client code needed!):
  ros2 service call /takeoff std_srvs/srv/Trigger {}
  ros2 service call /land    std_srvs/srv/Trigger {}

Or run the Python client:
  ros2 run drone_delivery_system takeoff_service_client
  ros2 run drone_delivery_system takeoff_service_client land
"""

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from std_msgs.msg import String


class TakeoffServiceServer(Node):
    """Handles takeoff and landing command services."""

    def __init__(self):
        super().__init__('takeoff_service_server')

        self.is_airborne    = False
        self.current_alt    = 0.0
        self.target_alt     = 50.0

        # Publish state changes so drone_status_node can update
        self.state_pub = self.create_publisher(String, '/drone_state_command', 10)

        # ── Service Server 1: /takeoff ────────────────────────────────────────
        # create_service(type, name, callback)
        # The callback is called automatically when a client calls the service
        self.takeoff_srv = self.create_service(
            Trigger,
            '/takeoff',
            self.takeoff_callback
        )

        # ── Service Server 2: /land ───────────────────────────────────────────
        self.land_srv = self.create_service(
            Trigger,
            '/land',
            self.land_callback
        )

        self.get_logger().info('=' * 45)
        self.get_logger().info('  Takeoff/Land Service Server — READY')
        self.get_logger().info('  Services: /takeoff, /land')
        self.get_logger().info('=' * 45)

    def takeoff_callback(self, request, response):
        """
        Called when a client calls /takeoff.

        Args:
            request  — Trigger.Request (empty for Trigger)
            response — Trigger.Response to fill in and return

        Returns:
            response — MUST always return this
        """
        if self.is_airborne:
            # Reject: already flying
            response.success = False
            response.message = (
                '❌ REJECTED: Already airborne at '
                f'{self.current_alt:.0f}m. Land first.'
            )
            self.get_logger().warn('Takeoff rejected — already airborne')
        else:
            # Accept: execute takeoff
            self.is_airborne  = True
            self.current_alt  = self.target_alt
            response.success  = True
            response.message  = (
                f'✅ TAKEOFF CONFIRMED: Ascending to {self.target_alt}m. '
                'All pre-flight checks passed.'
            )
            self._set_state('TAKING_OFF')
            self.get_logger().info(f'🚀 TAKEOFF! Ascending to {self.target_alt}m')

        return response     # ← NEVER forget this!

    def land_callback(self, request, response):
        """Called when a client calls /land."""
        if not self.is_airborne:
            response.success = False
            response.message = '❌ REJECTED: Drone is already on the ground.'
            self.get_logger().warn('Land rejected — already grounded')
        else:
            self.is_airborne = False
            self.current_alt = 0.0
            response.success = True
            response.message = '✅ LANDING: Initiating descent sequence.'
            self._set_state('LANDING')
            self.get_logger().info('🛬 LANDING! Descending...')

        return response

    def _set_state(self, state):
        msg      = String()
        msg.data = state
        self.state_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TakeoffServiceServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Service Server shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
