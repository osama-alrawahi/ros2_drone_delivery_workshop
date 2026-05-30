#!/usr/bin/env python3
"""
battery_monitor_node.py
=======================
WORKSHOP PART 4 — CREATE NODES  |  PART 8 — PARAMETERS

Simulates a drone battery management system (BMS).
In a real drone this reads voltage/current from hardware via I2C or CAN bus.

Topics Published:
  /battery_status   (std_msgs/Float32)  — Battery % (0.0–100.0)

Parameters (set at launch or live with ros2 param set):
  battery_warning_threshold  float  20.0   — Warn below this %
  initial_battery            float  100.0  — Starting charge
  discharge_rate             float  0.5    — % drained per second

Run:
  ros2 run drone_delivery_system battery_monitor_node

Override parameters at run:
  ros2 run drone_delivery_system battery_monitor_node \
    --ros-args -p discharge_rate:=2.0 -p battery_warning_threshold:=30.0

Live update while running:
  ros2 param set /battery_monitor_node discharge_rate 5.0
"""

import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class BatteryMonitorNode(Node):
    """Simulates and publishes drone battery percentage."""

    def __init__(self):
        super().__init__('battery_monitor_node')

        # ── Declare Parameters ────────────────────────────────────────────────
        # Parameters make values configurable at launch or runtime
        self.declare_parameter('battery_warning_threshold', 20.0)
        self.declare_parameter('initial_battery', 100.0)
        self.declare_parameter('discharge_rate', 0.5)

        # ── Read Parameters ───────────────────────────────────────────────────
        self.warning_threshold = (
            self.get_parameter('battery_warning_threshold')
            .get_parameter_value().double_value
        )
        self.battery_level = (
            self.get_parameter('initial_battery')
            .get_parameter_value().double_value
        )
        self.discharge_rate = (
            self.get_parameter('discharge_rate')
            .get_parameter_value().double_value
        )

        # ── Publisher ─────────────────────────────────────────────────────────
        self.battery_publisher = self.create_publisher(
            Float32,
            '/battery_status',
            10
        )

        # ── Timer ─────────────────────────────────────────────────────────────
        # Publish every 2 seconds (0.5 Hz — real BMS systems typically 1–10 Hz)
        self.timer = self.create_timer(2.0, self.publish_battery)

        self.get_logger().info('=' * 45)
        self.get_logger().info('  Battery Monitor Node — ONLINE')
        self.get_logger().info('=' * 45)
        self.get_logger().info(f'  Initial charge  : {self.battery_level:.1f}%')
        self.get_logger().info(f'  Discharge rate  : {self.discharge_rate:.1f}%/s')
        self.get_logger().info(f'  Warning at      : {self.warning_threshold:.1f}%')
        self.get_logger().info('=' * 45)

    def publish_battery(self):
        """
        Timer callback — simulate discharge and publish.
        Re-reads 'discharge_rate' every call so live ros2 param set works.
        """
        # Re-read in case it was changed with ros2 param set
        self.discharge_rate = (
            self.get_parameter('discharge_rate')
            .get_parameter_value().double_value
        )
        self.warning_threshold = (
            self.get_parameter('battery_warning_threshold')
            .get_parameter_value().double_value
        )

        # Drain: 2 seconds elapsed × discharge_rate %/s
        self.battery_level -= self.discharge_rate * 2.0
        self.battery_level = max(0.0, self.battery_level)

        # Small noise simulates real sensor readings
        display = max(0.0, min(100.0, self.battery_level + random.uniform(-0.2, 0.2)))

        # Build and publish message
        msg = Float32()
        msg.data = display
        self.battery_publisher.publish(msg)

        # Colourful log with ASCII battery bar
        bar = self._battery_bar(display)
        if display <= self.warning_threshold:
            self.get_logger().warn(f'🔴 LOW BATTERY! {display:.1f}% {bar} ← RTH Recommended!')
        elif display <= 50.0:
            self.get_logger().warn(f'🟡 Battery: {display:.1f}% {bar}')
        else:
            self.get_logger().info(f'🟢 Battery: {display:.1f}% {bar}')

    def _battery_bar(self, level):
        """Return a visual ASCII battery bar."""
        filled = int(level / 10)
        return f'[{"█" * filled}{"░" * (10 - filled)}]'


def main(args=None):
    rclpy.init(args=args)
    node = BatteryMonitorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Battery Monitor shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
