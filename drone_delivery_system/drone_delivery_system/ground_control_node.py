#!/usr/bin/env python3
"""
ground_control_node.py
======================
WORKSHOP PART 5 — TOPICS (PUBLISHER / SUBSCRIBER)

Ground control station — subscribes to ALL drone telemetry and
displays a live dashboard. Demonstrates multiple subscribers in one node.

Topics Subscribed:
  /battery_status   (std_msgs/Float32)      — Battery %
  /gps_location     (sensor_msgs/NavSatFix) — GPS coordinates
  /drone_status     (std_msgs/String)       — Operational state

Run:
  ros2 run drone_delivery_system ground_control_node

Key concepts demonstrated:
  - Three separate subscribers in one node
  - Callback functions that store received data
  - Timer that reads stored data and displays a dashboard
  - Asynchronous: each callback fires independently
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from sensor_msgs.msg import NavSatFix


class GroundControlNode(Node):
    """Ground control station — monitors all drone telemetry."""

    def __init__(self):
        super().__init__('ground_control_node')

        # ── Telemetry storage ─────────────────────────────────────────────────
        # None until the first message arrives on each topic
        self.battery_level  = None
        self.gps_data       = None
        self.drone_status   = None
        self.msg_counts     = {'battery': 0, 'gps': 0, 'status': 0}

        # ── Subscriber 1: Battery ─────────────────────────────────────────────
        self.battery_sub = self.create_subscription(
            Float32,
            '/battery_status',
            self.battery_callback,    # ← runs every time a battery msg arrives
            10
        )

        # ── Subscriber 2: GPS ────────────────────────────────────────────────
        self.gps_sub = self.create_subscription(
            NavSatFix,
            '/gps_location',
            self.gps_callback,        # ← runs every time a GPS msg arrives
            10
        )

        # ── Subscriber 3: Drone Status ────────────────────────────────────────
        self.status_sub = self.create_subscription(
            String,
            '/drone_status',
            self.status_callback,     # ← runs every time a status msg arrives
            10
        )

        # ── Timer: Dashboard refresh ──────────────────────────────────────────
        # Shows latest stored telemetry every 3 seconds
        self.timer = self.create_timer(3.0, self.display_dashboard)

        self.get_logger().info('🛰️  Ground Control Station — ONLINE')
        self.get_logger().info('   Monitoring: /battery_status | /gps_location | /drone_status')
        self.get_logger().info('   Waiting for drone telemetry...')

    # ── Callbacks ─────────────────────────────────────────────────────────────
    # Each callback runs AUTOMATICALLY when a message arrives.
    # They just store the data; the dashboard timer reads it periodically.

    def battery_callback(self, msg):
        """Called every time battery_monitor_node publishes (every 2 s)."""
        self.battery_level = msg.data           # msg.data = float value
        self.msg_counts['battery'] += 1

    def gps_callback(self, msg):
        """Called every time gps_node publishes (every 1 s)."""
        self.gps_data = msg                     # full NavSatFix message
        self.msg_counts['gps'] += 1

    def status_callback(self, msg):
        """Called every time drone_status_node publishes (every 1 s)."""
        self.drone_status = msg.data            # msg.data = string value
        self.msg_counts['status'] += 1

    # ── Dashboard ─────────────────────────────────────────────────────────────

    def display_dashboard(self):
        """Timer callback — print the latest telemetry as a dashboard."""
        sep = '─' * 50
        self.get_logger().info('\n' + '═' * 50)
        self.get_logger().info('         🚁  GROUND CONTROL DASHBOARD  🚁')
        self.get_logger().info('═' * 50)

        # Status
        STATE_EMOJI = {
            'IDLE': '⏸️ ', 'TAKING_OFF': '🚀', 'FLYING': '✈️ ',
            'DELIVERING': '📦', 'RETURNING': '🔄', 'LANDING': '🛬',
        }
        if self.drone_status:
            emoji = STATE_EMOJI.get(self.drone_status, '❓')
            self.get_logger().info(f'  {emoji} Status    : {self.drone_status}')
        else:
            self.get_logger().info('  ❓ Status    : No signal...')

        # Battery
        if self.battery_level is not None:
            bar    = self._bar(self.battery_level)
            health = '⚠️ LOW' if self.battery_level < 20 else '✅ OK'
            self.get_logger().info(f'  🔋 Battery   : {self.battery_level:.1f}% {bar} {health}')
        else:
            self.get_logger().info('  🔋 Battery   : No signal...')

        # GPS
        if self.gps_data:
            self.get_logger().info(f'  📍 GPS Lat   : {self.gps_data.latitude:.6f}°')
            self.get_logger().info(f'  📍 GPS Lon   : {self.gps_data.longitude:.6f}°')
            self.get_logger().info(f'  🏔️  Altitude  : {self.gps_data.altitude:.1f} m')
        else:
            self.get_logger().info('  📍 GPS       : No signal...')

        # Message stats
        self.get_logger().info(sep)
        self.get_logger().info(
            f'  📊 Messages  : '
            f'Battery={self.msg_counts["battery"]} | '
            f'GPS={self.msg_counts["gps"]} | '
            f'Status={self.msg_counts["status"]}'
        )
        self.get_logger().info('═' * 50)

    def _bar(self, level):
        filled = int(level / 10)
        return f'[{"█" * filled}{"░" * (10 - filled)}]'


def main(args=None):
    rclpy.init(args=args)
    node = GroundControlNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Ground Control shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
