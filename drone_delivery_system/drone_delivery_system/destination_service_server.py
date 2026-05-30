#!/usr/bin/env python3
"""
destination_service_server.py
=============================
WORKSHOP PART 6 — SERVICES (Custom Interface)

Allows ground control to change the delivery destination in real time.
Uses our CUSTOM ChangeDestination service (drone_delivery_interfaces).

Service:
  /change_destination  (drone_delivery_interfaces/ChangeDestination)

Run:
  ros2 run drone_delivery_system destination_service_server

Test with CLI:
  ros2 service call /change_destination \
    drone_delivery_interfaces/srv/ChangeDestination \
    "{latitude: 23.6097, longitude: 58.1804, destination_name: 'SQU'}"

Or run the client:
  ros2 run drone_delivery_system destination_service_client
"""

import rclpy
from rclpy.node import Node
from drone_delivery_interfaces.srv import ChangeDestination


class DestinationServiceServer(Node):
    """Manages and updates the active delivery destination."""

    KNOWN_LOCATIONS = {
        'Home Base':                  (23.5880, 58.3829),
        'Sultan Qaboos University':   (23.6097, 58.1804),
        'Muscat City Centre':         (23.5957, 58.2772),
        'Royal Opera House':          (23.6134, 58.5928),
        'Muttrah Corniche':           (23.6177, 58.5902),
    }

    def __init__(self):
        super().__init__('destination_service_server')

        # Current destination
        self.destination = {
            'name':      'Home Base',
            'latitude':  23.5880,
            'longitude': 58.3829,
        }

        # ── Service Server ────────────────────────────────────────────────────
        self.srv = self.create_service(
            ChangeDestination,          # Our CUSTOM service type
            '/change_destination',
            self.change_destination_callback
        )

        self.get_logger().info('=' * 50)
        self.get_logger().info('  Destination Service Server — READY')
        self.get_logger().info(f'  Current: {self.destination["name"]}')
        self.get_logger().info('  Known locations:')
        for name, (lat, lon) in self.KNOWN_LOCATIONS.items():
            self.get_logger().info(f'    • {name}: ({lat:.4f}, {lon:.4f})')
        self.get_logger().info('=' * 50)

    def change_destination_callback(self, request, response):
        """
        Called when a client sends a ChangeDestination request.

        Request fields:
          request.latitude          Target latitude
          request.longitude         Target longitude
          request.destination_name  Human-readable name

        Response fields:
          response.success               True/False
          response.message               Confirmation text
          response.previous_destination  Name of old destination
        """
        previous = self.destination['name']

        # ── Validate coordinates ──────────────────────────────────────────────
        if not (-90.0 <= request.latitude <= 90.0):
            response.success              = False
            response.message              = f'❌ Invalid latitude: {request.latitude}'
            response.previous_destination = previous
            return response

        if not (-180.0 <= request.longitude <= 180.0):
            response.success              = False
            response.message              = f'❌ Invalid longitude: {request.longitude}'
            response.previous_destination = previous
            return response

        # ── Update destination ────────────────────────────────────────────────
        distance = self._rough_distance(
            self.destination['latitude'], self.destination['longitude'],
            request.latitude, request.longitude
        )

        self.destination = {
            'name':      request.destination_name,
            'latitude':  request.latitude,
            'longitude': request.longitude,
        }

        response.success              = True
        response.previous_destination = previous
        response.message = (
            f'✅ Destination updated!\n'
            f'   Previous : {previous}\n'
            f'   New      : {request.destination_name}\n'
            f'   Coords   : ({request.latitude:.4f}°N, {request.longitude:.4f}°E)\n'
            f'   Distance : ~{distance:.1f} km from previous'
        )

        self.get_logger().info(
            f'📍 {previous} → {request.destination_name}'
        )
        return response

    def _rough_distance(self, lat1, lon1, lat2, lon2):
        """Rough flat-earth distance in km (good enough for a workshop demo)."""
        dlat = abs(lat2 - lat1) * 111.0
        dlon = abs(lon2 - lon1) * 111.0 * 0.85
        return (dlat ** 2 + dlon ** 2) ** 0.5


def main(args=None):
    rclpy.init(args=args)
    node = DestinationServiceServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Destination Service shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
