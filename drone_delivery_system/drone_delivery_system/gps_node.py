#!/usr/bin/env python3
"""
gps_node.py
===========
WORKSHOP PART 4 — CREATE NODES

Simulates a GPS receiver publishing standard NavSatFix messages.
In a real drone this reads from serial/USB GPS (ublox, Garmin, etc.)
via the nmea_navsat_driver or ublox ROS2 driver — same topic/message type.

Topics Published:
  /gps_location   (sensor_msgs/NavSatFix)  — GPS coordinates

Parameters:
  home_latitude   float  23.5880   — Home base latitude (Muscat, Oman)
  home_longitude  float  58.3829   — Home base longitude
  home_altitude   float  50.0      — Altitude in metres

Run:
  ros2 run drone_delivery_system gps_node

Watch the output:
  ros2 topic echo /gps_location
  ros2 topic hz   /gps_location
"""

import math
import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix, NavSatStatus


class GPSNode(Node):
    """Simulates a GPS receiver and publishes coordinates."""

    def __init__(self):
        super().__init__('gps_node')

        # ── Parameters ────────────────────────────────────────────────────────
        # Defaults to Muscat, Oman — change at launch with -p home_latitude:=...
        self.declare_parameter('home_latitude',  23.5880)
        self.declare_parameter('home_longitude', 58.3829)
        self.declare_parameter('home_altitude',  50.0)

        self.home_lat = self.get_parameter('home_latitude').get_parameter_value().double_value
        self.home_lon = self.get_parameter('home_longitude').get_parameter_value().double_value
        self.home_alt = self.get_parameter('home_altitude').get_parameter_value().double_value

        # Current position (starts at home)
        self.current_lat = self.home_lat
        self.current_lon = self.home_lon
        self.current_alt = self.home_alt

        self.start_time = time.time()

        # ── Publisher ─────────────────────────────────────────────────────────
        # NavSatFix is the STANDARD ROS2 GPS message — used by all GPS drivers
        # Using it here means zero code changes when switching to real hardware
        self.gps_publisher = self.create_publisher(
            NavSatFix,
            '/gps_location',
            10
        )

        # ── Timer ─────────────────────────────────────────────────────────────
        # 1 Hz — real GPS modules typically output 1–10 Hz
        self.timer = self.create_timer(1.0, self.publish_gps)

        self.get_logger().info('=' * 45)
        self.get_logger().info('  GPS Node — ONLINE')
        self.get_logger().info('=' * 45)
        self.get_logger().info(f'  Home: {self.home_lat:.6f}°N, {self.home_lon:.6f}°E')
        self.get_logger().info(f'  Altitude: {self.home_alt:.1f} m')
        self.get_logger().info('=' * 45)

    def publish_gps(self):
        """
        Timer callback — simulate position and publish NavSatFix.
        Simulates slight circular GPS drift around home position.
        """
        elapsed = time.time() - self.start_time

        # Simulate slow drift (tiny circle ~5.5 m radius)
        drift = 0.00005
        lat_offset = drift * math.sin(elapsed * 0.05)
        lon_offset = drift * math.cos(elapsed * 0.05)

        # ── Build the NavSatFix message ───────────────────────────────────────
        msg = NavSatFix()

        # Timestamp and coordinate frame
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'gps_frame'

        # GPS fix status
        msg.status.status  = NavSatStatus.STATUS_FIX   # Has a valid fix
        msg.status.service = NavSatStatus.SERVICE_GPS  # Using GPS constellation

        # Position
        msg.latitude  = self.current_lat + lat_offset
        msg.longitude = self.current_lon + lon_offset
        msg.altitude  = self.current_alt

        # Position covariance — uncertainty in metres²
        # Diagonal: [lat_variance, lon_variance, alt_variance, ...]
        msg.position_covariance = [
            0.1, 0.0, 0.0,
            0.0, 0.1, 0.0,
            0.0, 0.0, 0.5,
        ]
        msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN

        self.gps_publisher.publish(msg)

        self.get_logger().info(
            f'📍 GPS: {msg.latitude:.6f}°N, '
            f'{msg.longitude:.6f}°E, '
            f'Alt: {msg.altitude:.1f}m'
        )

    def update_position(self, lat, lon, alt=None):
        """
        Update the simulated position.
        Can be called by the delivery action server to move the drone.
        """
        self.current_lat = lat
        self.current_lon = lon
        if alt is not None:
            self.current_alt = alt


def main(args=None):
    rclpy.init(args=args)
    node = GPSNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('GPS Node shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
