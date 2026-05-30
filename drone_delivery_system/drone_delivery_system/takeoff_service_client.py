#!/usr/bin/env python3
"""
takeoff_service_client.py
=========================
WORKSHOP PART 6 — SERVICES

Sends takeoff or landing commands to the service server.

Usage:
  ros2 run drone_delivery_system takeoff_service_client         # Takeoff
  ros2 run drone_delivery_system takeoff_service_client land    # Land
"""

import sys
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class TakeoffServiceClient(Node):
    """Client that calls /takeoff or /land services."""

    def __init__(self):
        super().__init__('takeoff_service_client')

        # ── Service Clients ───────────────────────────────────────────────────
        # These CALL services — they don't provide them
        self.takeoff_client = self.create_client(Trigger, '/takeoff')
        self.land_client    = self.create_client(Trigger, '/land')

    def send_takeoff(self):
        """Send a takeoff request and wait for response."""
        self.get_logger().info('📡 Sending TAKEOFF command...')
        return self._call(self.takeoff_client, '/takeoff')

    def send_land(self):
        """Send a land request and wait for response."""
        self.get_logger().info('📡 Sending LAND command...')
        return self._call(self.land_client, '/land')

    def _call(self, client, name):
        """Generic helper: wait for service, call it, log response."""
        # Block until the service server is available (max 5 s)
        if not client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error(
                f'❌ {name} service not available! Is the server running?'
            )
            return None

        # Create and send request asynchronously (returns a Future)
        future = client.call_async(Trigger.Request())

        # Block until the Future resolves (response received)
        rclpy.spin_until_future_complete(self, future)

        response = future.result()
        if response.success:
            self.get_logger().info(f'✅ {response.message}')
        else:
            self.get_logger().error(f'❌ {response.message}')
        return response


def main(args=None):
    rclpy.init(args=args)
    client = TakeoffServiceClient()

    if len(sys.argv) > 1 and sys.argv[1].lower() == 'land':
        client.send_land()
    else:
        client.send_takeoff()

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
