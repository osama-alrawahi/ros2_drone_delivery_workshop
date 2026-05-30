#!/usr/bin/env python3
"""
drone_delivery.launch.py
========================
WORKSHOP PART 9 — LAUNCH FILES

Starts the entire Drone Delivery System with one command:
  ros2 launch drone_delivery_system drone_delivery.launch.py

Optional overrides:
  drone_speed:=20.0          Cruising speed m/s
  max_altitude:=150.0        Max altitude m
  battery_warning:=25.0      Warn below this battery %
  home_latitude:=23.5880     Home base latitude
  home_longitude:=58.3829    Home base longitude
  discharge_rate:=0.5        Battery drain rate %/s

Example:
  ros2 launch drone_delivery_system drone_delivery.launch.py \
    drone_speed:=25.0 battery_warning:=30.0
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, LogInfo, TimerAction
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    """
    ROS2 calls this function to get the launch description.
    Must be named exactly 'generate_launch_description'.
    Must return a LaunchDescription object.
    """

    # ── Declare launch arguments ──────────────────────────────────────────────
    # These become command-line options: ros2 launch ... key:=value
    args = [
        DeclareLaunchArgument('drone_speed',     default_value='15.0',    description='Cruise speed m/s'),
        DeclareLaunchArgument('max_altitude',    default_value='120.0',   description='Max altitude m'),
        DeclareLaunchArgument('battery_warning', default_value='20.0',    description='Low battery warning %'),
        DeclareLaunchArgument('home_latitude',   default_value='23.5880', description='Home base latitude'),
        DeclareLaunchArgument('home_longitude',  default_value='58.3829', description='Home base longitude'),
        DeclareLaunchArgument('discharge_rate',  default_value='0.3',     description='Battery drain %/s'),
    ]

    # ── Reference argument values ─────────────────────────────────────────────
    drone_speed     = LaunchConfiguration('drone_speed')
    max_altitude    = LaunchConfiguration('max_altitude')
    battery_warning = LaunchConfiguration('battery_warning')
    home_lat        = LaunchConfiguration('home_latitude')
    home_lon        = LaunchConfiguration('home_longitude')
    discharge_rate  = LaunchConfiguration('discharge_rate')

    # ── Node definitions ──────────────────────────────────────────────────────

    drone_status_node = Node(
        package='drone_delivery_system',
        executable='drone_status_node',
        name='drone_status_node',
        output='screen',
        emulate_tty=True,
    )

    battery_monitor_node = Node(
        package='drone_delivery_system',
        executable='battery_monitor_node',
        name='battery_monitor_node',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'battery_warning_threshold': battery_warning,
            'initial_battery':           100.0,
            'discharge_rate':            discharge_rate,
        }],
    )

    gps_node = Node(
        package='drone_delivery_system',
        executable='gps_node',
        name='gps_node',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'home_latitude':  home_lat,
            'home_longitude': home_lon,
            'home_altitude':  50.0,
        }],
    )

    # Slight delay so telemetry nodes are publishing before the dashboard starts
    ground_control_node = TimerAction(
        period=1.5,
        actions=[Node(
            package='drone_delivery_system',
            executable='ground_control_node',
            name='ground_control_node',
            output='screen',
            emulate_tty=True,
        )],
    )

    takeoff_service_server = Node(
        package='drone_delivery_system',
        executable='takeoff_service_server',
        name='takeoff_service_server',
        output='screen',
        emulate_tty=True,
    )

    destination_service_server = Node(
        package='drone_delivery_system',
        executable='destination_service_server',
        name='destination_service_server',
        output='screen',
        emulate_tty=True,
    )

    delivery_action_server = Node(
        package='drone_delivery_system',
        executable='delivery_action_server',
        name='delivery_action_server',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'drone_speed_ms':      drone_speed,
            'max_altitude':        max_altitude,
            'delivery_hover_time': 10.0,
        }],
    )

    # ── Assemble LaunchDescription ────────────────────────────────────────────
    return LaunchDescription([
        # Pretty startup banner
        LogInfo(msg=''),
        LogInfo(msg='🚁 ═══════════════════════════════════════════════════'),
        LogInfo(msg='🚁    DRONE DELIVERY SYSTEM — LAUNCHING               '),
        LogInfo(msg='🚁 ═══════════════════════════════════════════════════'),
        LogInfo(msg=''),

        # Arguments must be declared before nodes that reference them
        *args,

        # Telemetry nodes (start first)
        drone_status_node,
        battery_monitor_node,
        gps_node,

        # Ground control (delayed)
        ground_control_node,

        # Service & action servers
        takeoff_service_server,
        destination_service_server,
        delivery_action_server,

        LogInfo(msg=''),
        LogInfo(msg='✅ All nodes launched! Try these commands in a new terminal:'),
        LogInfo(msg='   source ~/ros2_ws/install/setup.bash'),
        LogInfo(msg='   ros2 service call /takeoff std_srvs/srv/Trigger {}'),
        LogInfo(msg='   ros2 node list'),
        LogInfo(msg='   rqt_graph'),
        LogInfo(msg=''),
    ])
