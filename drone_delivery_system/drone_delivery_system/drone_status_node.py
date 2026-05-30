#!/usr/bin/env python3
"""
drone_status_node.py
====================
WORKSHOP PART 4 — CREATE NODES

Manages and publishes the operational state of the drone.

Valid States:
  IDLE        - Drone on ground, waiting for commands
  TAKING_OFF  - Drone ascending to cruise altitude
  FLYING      - Drone in transit to destination
  DELIVERING  - Drone lowering package at destination
  RETURNING   - Drone flying back to home base
  LANDING     - Drone descending to ground

Topics Published:
  /drone_status          (std_msgs/String)  — Current drone state

Topics Subscribed:
  /drone_state_command   (std_msgs/String)  — Commands to change state

Run:
  ros2 run drone_delivery_system drone_status_node
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DroneStatusNode(Node):
    """Manages and publishes the drone's operational state."""

    VALID_STATES = [
        'IDLE', 'TAKING_OFF', 'FLYING',
        'DELIVERING', 'RETURNING', 'LANDING'
    ]

    def __init__(self):
        # Call the parent Node constructor with our unique node name
        super().__init__('drone_status_node')

        # Drone starts idle on the ground
        self.current_state = 'IDLE'

        # ── Publisher ────────────────────────────────────────────────────────
        # Broadcasts current state to /drone_status every second
        self.status_publisher = self.create_publisher(
            String,           # Message type: a simple string
            '/drone_status',  # Topic name — MUST match subscriber
            10                # Queue size: buffer up to 10 messages
        )

        # ── Subscriber ───────────────────────────────────────────────────────
        # Listens for state change commands from other nodes
        self.state_subscriber = self.create_subscription(
            String,
            '/drone_state_command',
            self.state_command_callback,   # Called on every incoming message
            10
        )

        # ── Timer ────────────────────────────────────────────────────────────
        # Calls publish_status() every 1.0 second automatically
        self.timer = self.create_timer(1.0, self.publish_status)

        self.get_logger().info('=' * 45)
        self.get_logger().info('  Drone Status Node — ONLINE')
        self.get_logger().info('=' * 45)
        self.get_logger().info(f'  Initial state : {self.current_state}')
        self.get_logger().info(f'  Publishing on : /drone_status')
        self.get_logger().info(f'  Listening on  : /drone_state_command')
        self.get_logger().info('=' * 45)

    def state_command_callback(self, msg):
        """
        Callback — called automatically whenever a message arrives on
        /drone_state_command. Updates the current state if valid.
        """
        new_state = msg.data.upper().strip()

        if new_state in self.VALID_STATES:
            old_state = self.current_state
            self.current_state = new_state
            self.get_logger().info(
                f'State transition: {old_state} → {new_state}'
            )
        else:
            self.get_logger().warn(
                f'Invalid command: "{new_state}". '
                f'Valid states: {self.VALID_STATES}'
            )

    def publish_status(self):
        """Timer callback — publishes the current state every 1 second."""
        msg = String()
        msg.data = self.current_state
        self.status_publisher.publish(msg)
        self.get_logger().info(f'📡 Status: [{self.current_state}]')


def main(args=None):
    """Entry point. Every ROS2 Python node follows this exact pattern."""
    rclpy.init(args=args)
    node = DroneStatusNode()

    try:
        rclpy.spin(node)          # Block here — process all callbacks
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
