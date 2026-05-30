#!/usr/bin/env python3
"""
destination_service_client.py
=============================
WORKSHOP PART 6 — SERVICES (Custom Interface)

Changes the drone's active delivery destination.

Usage:
  ros2 run drone_delivery_system destination_service_client

Or via CLI (no client code needed):
  ros2 service call /change_destination \
    drone_delivery_interfaces/srv/ChangeDestination \
    "{latitude: 23.6097, longitude: 58.1804, destination_name: 'SQU'}"
"""

import rclpy
from rclpy.node import Node
from drone_delivery_interfaces.srv import ChangeDestination


class DestinationServiceClient(Node):
    """Client to update the delivery destination."""

    def __init__(self):
        super().__init__('destination_service_client')

        self.client = self.create_client(
            ChangeDestination,
            '/change_destination'
        )

    def change_destination(self, name, latitude, longitude):
        """Send a ChangeDestination request and wait for response."""
        self.get_logger().info(f'📡 Requesting destination change → {name}')

        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('❌ /change_destination not available!')
            return None

        # Build the CUSTOM request object
        request                  = ChangeDestination.Request()
        request.destination_name = name
        request.latitude         = latitude
        request.longitude        = longitude

        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        response = future.result()
        if response.success:
            self.get_logger().info(response.message)
        else:
            self.get_logger().error(response.message)
        return response


def main(args=None):
    rclpy.init(args=args)
    client = DestinationServiceClient()

    # Send destination change to Sultan Qaboos University
    client.change_destination(
        name='Sultan Qaboos University',
        latitude=23.6097,
        longitude=58.1804,
    )

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
