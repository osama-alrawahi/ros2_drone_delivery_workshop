# 🚁 ROS2 Drone Delivery System — Complete Beginner Workshop
### *Build a Real Autonomous Drone Delivery System with ROS2 Jazzy*

---

> **Workshop Level:** Absolute Beginner  
> **Duration:** 2–3 Hours  
> **Prerequisites:** Basic Python, Ubuntu terminal familiarity  
> **ROS2 Version:** Jazzy Jalisco (LTS)  
> **Platform:** Ubuntu 24.04 LTS

---

## 🗂️ TABLE OF CONTENTS

| Part | Topic | Duration |
|------|-------|----------|
| 1 | Introduction to ROS2 | 15 min |
| 2 | Create ROS2 Workspace | 10 min |
| 3 | Create the Package | 10 min |
| 4 | Create Nodes | 20 min |
| 5 | Topics (Publisher/Subscriber) | 25 min |
| 6 | Services | 20 min |
| 7 | Actions | 25 min |
| 8 | Parameters | 10 min |
| 9 | Launch Files | 10 min |
| 10 | Visualization & Debugging | 15 min |
| 11 | Final Integrated Demo | 20 min |
| 12 | Workshop Materials & Exercises | — |
| 13 | Advanced Bonus & Next Steps | — |

---

# PART 1 — INTRODUCTION TO ROS2

## 🤔 What is ROS2?

**ROS2 (Robot Operating System 2)** is NOT an operating system. It is a **middleware framework** — a collection of tools, libraries, and conventions that help you build complex robot software faster, cleaner, and more reliably.

Think of ROS2 as the **nervous system of a robot**. It handles:
- How different parts of the robot **communicate** with each other
- How to **run many programs simultaneously** and have them talk
- How to **debug, visualize, and test** your robot software
- How to **reuse code** across projects and robots

### Why ROS2 for Drones?

| Feature | Without ROS2 | With ROS2 |
|---------|-------------|-----------|
| GPS + Flight Controller communication | Write custom protocols | Topics (plug and play) |
| Long delivery missions | Complex state machines | Actions (built-in) |
| Dynamic speed control | Restart the whole system | Parameters (live update) |
| Multi-node debugging | Print statements everywhere | rqt_graph, ros2 doctor |
| Reusing sensors | Rewrite sensor drivers | Import standard packages |

### Real Drones Using ROS2
- **Amazon Prime Air** — delivery drones, ROS-based middleware
- **Zipline** — medical supply drones in Africa
- **DJI Enterprise** — inspection drones with ROS2 bridges
- **PX4 Autopilot** — open-source flight controller with full ROS2 support
- **Ardupilot** — ROS2/MAVROS integration for autonomous flight

---

## 🏗️ ROS2 Core Concepts

### 1. Nodes

A **node** is a single executable program with one specific job. ROS2 robots are built from many small nodes working together.

```
Drone Example:
┌─────────────────────────────────────────────────┐
│                 DRONE SYSTEM                     │
│                                                  │
│  [GPS Node]    [Battery Node]   [Camera Node]   │
│  Reads GPS     Reads battery    Reads camera     │
│  sensor        voltage          frames           │
│                                                  │
│  [Flight Controller Node]  [Delivery Node]      │
│  Controls motors           Manages missions      │
└─────────────────────────────────────────────────┘
```

**Why separate nodes?**
- Each node can be **restarted independently** (GPS crashes? Restart only GPS node)
- Nodes can run on **different computers** (flight controller on Raspberry Pi, AI on GPU)
- Easy to **add or remove features** without touching other code

### 2. Topics

Topics are **communication channels** for continuous data streams. One node **publishes** data, many nodes can **subscribe** to receive it.

```
Publisher → Topic → Subscriber(s)

[GPS Node] ──publishes──→ /gps_location ──subscribes──→ [Ground Control]
                                         ──subscribes──→ [Navigation Node]
                                         ──subscribes──→ [Logging Node]
```

**When to use topics:**
- Battery percentage (updates every second)
- GPS coordinates (continuous stream)
- Camera frames (high-frequency data)
- Drone status updates

### 3. Services

Services are **request/response** communications. Like making a phone call — one side asks, the other answers.

```
Client ──── Request ────→ Server
Client ←─── Response ─── Server

[Ground Control] ──takeoff request──→ [Flight Controller]
[Ground Control] ←──"Drone airborne"── [Flight Controller]
```

**When to use services:**
- Takeoff/Land commands
- Change destination
- Query system status
- One-time configuration

### 4. Actions

Actions are for **long-running tasks** with progress feedback. Like sending a package — you get updates along the way.

```
Client ──── Goal ──────────────→ ActionServer
Client ←─── Feedback (ongoing) ── ActionServer
Client ←─── Result (final) ────── ActionServer

[Ground Control] ──"Deliver to SQU"──→ [Delivery Server]
[Ground Control] ←── "30% - Flying" ── [Delivery Server]
[Ground Control] ←── "60% - Delivering" [Delivery Server]
[Ground Control] ←── "Delivered! ✓" ─── [Delivery Server]
```

**When to use actions:**
- Complete delivery missions
- Navigation tasks (go to waypoint)
- Mapping (scan an area)
- Any task taking more than a few seconds

### 5. Parameters

Parameters are **configuration values** that can be changed at runtime without restarting.

```
[Delivery Node]
  - drone_speed: 15.0 m/s    ← Can change while running!
  - max_altitude: 120.0 m
  - battery_warning: 20.0 %
```

---

## 📐 Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DRONE DELIVERY SYSTEM                        │
│                                                                 │
│  ┌────────────────┐    Topics      ┌──────────────────────┐    │
│  │   GPS NODE     │──/gps_location─→│                      │    │
│  └────────────────┘                │                      │    │
│                                    │   GROUND CONTROL     │    │
│  ┌────────────────┐    Topics      │      NODE            │    │
│  │ BATTERY NODE   │──/battery_status→  (Dashboard)        │    │
│  └────────────────┘                │                      │    │
│                                    │                      │    │
│  ┌────────────────┐    Topics      │                      │    │
│  │  STATUS NODE   │──/drone_status─→                      │    │
│  └────────────────┘                └──────────────────────┘    │
│                                                                 │
│  ┌────────────────────┐  Services                              │
│  │ TAKEOFF/LAND SRV   │──/takeoff, /land ← Ground Control     │
│  └────────────────────┘                                        │
│                                                                 │
│  ┌────────────────────┐  Services                              │
│  │ DESTINATION SRV    │──/change_destination ← Ground Control  │
│  └────────────────────┘                                        │
│                                                                 │
│  ┌────────────────────┐  Actions                               │
│  │  DELIVERY ACTION   │──/deliver_package ← Ground Control     │
│  │      SERVER        │   (goal/feedback/result)               │
│  └────────────────────┘                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔌 DDS — How Nodes Communicate

ROS2 uses **DDS (Data Distribution Service)** — an industrial communication standard.

**Key DDS Properties:**
- **Decentralized** — No central server can crash and break everything
- **Discovery** — Nodes automatically find each other on the network
- **QoS** — Quality of Service settings for reliability, latency
- **Real-time capable** — Used in military, aerospace, medical systems

```
Traditional System:        ROS2 with DDS:
  [Central Server]          [Node A] ←──→ [Node B]
   ↑    ↑    ↑                 ↑               ↑
[A] [B] [C]               [Node C] ←──→ [Node D]
Server fails = ALL fail    Any node fails = others continue
```

---

# PART 2 — CREATE ROS2 WORKSPACE

## What is a Workspace?

A **workspace** is a folder where you keep all your ROS2 packages. Think of it as a project folder that ROS2 understands.

```
~/ros2_ws/          ← Your workspace (root)
├── src/            ← Your SOURCE CODE goes here
├── build/          ← Auto-generated: compilation files
├── install/        ← Auto-generated: ready-to-run packages
└── log/            ← Auto-generated: build logs
```

> **Rule:** You ONLY touch `src/`. ROS2 manages build/, install/, log/ automatically.

## Step-by-Step Workspace Setup

### Step 1: Source ROS2

Every terminal session needs ROS2 sourced. Add this to `~/.bashrc` so it's automatic:

```bash
# Source ROS2 Jazzy
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Verify ROS2 is working
ros2 --version
```

**Expected output:**
```
ros2 cli version: 0.18.x
```

### Step 2: Create the Workspace

```bash
# Create the workspace with src/ folder
mkdir -p ~/ros2_ws/src

# Enter the workspace
cd ~/ros2_ws

# Build it (empty build — creates install/ and build/ folders)
colcon build

# Source the workspace
source install/setup.bash
```

**What `colcon build` does:**
- `colcon` = **CO**mpile **L**ocal packages with **COL**on dependencies
- Finds all packages in `src/`
- Compiles them in the right order
- Installs them to `install/`

**Expected output:**
```
Starting >>> (nothing yet — no packages)
Summary: 0 packages finished [0.12s]
```

### Step 3: Make Sourcing Permanent

```bash
# Add workspace source to bashrc (run ONCE)
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Step 4: Understanding Each Folder

```bash
ls ~/ros2_ws/
```

```
build/    ← CMake/colcon build artifacts. Safe to delete.
install/  ← Installed packages. Safe to delete (rebuild to restore).
log/      ← Build and run logs. Safe to delete.
src/      ← YOUR CODE. NEVER delete this!
```

### How to Clean/Reset the Workspace

```bash
# Safe clean (keeps src/)
cd ~/ros2_ws
rm -rf build/ install/ log/

# Rebuild from scratch
colcon build

# Re-source
source install/setup.bash
```

> ⚠️ **Never** run `rm -rf ~/ros2_ws/src/` — that deletes your code!

### Tip: Useful Shell Aliases

Add to `~/.bashrc` for convenience:

```bash
# Add these to ~/.bashrc
alias cdws='cd ~/ros2_ws'
alias cbs='cd ~/ros2_ws && colcon build --symlink-install && source install/setup.bash'
alias sourceros='source ~/ros2_ws/install/setup.bash'
```

---

# PART 3 — CREATE THE PACKAGE

## Package Concepts

A **package** is the unit of code organization in ROS2. Each package:
- Has a unique name
- Lists its dependencies
- Contains nodes, messages, services, etc.

## Creating Two Packages

Our system needs **two packages**:
1. `drone_delivery_interfaces` — Custom message/service/action definitions
2. `drone_delivery_system` — All our Python nodes

### Step 1: Create the Interfaces Package

```bash
cd ~/ros2_ws/src

# Create a CMake package for interfaces (interfaces always use CMake)
ros2 pkg create drone_delivery_interfaces \
    --build-type ament_cmake \
    --dependencies rosidl_default_generators std_msgs action_msgs
```

**What this command does:**
- `ros2 pkg create` — Create new ROS2 package
- `drone_delivery_interfaces` — Package name
- `--build-type ament_cmake` — Uses CMake (required for custom interfaces)
- `--dependencies` — Other packages this one needs

### Step 2: Create Service Definition

```bash
mkdir -p ~/ros2_ws/src/drone_delivery_interfaces/srv
mkdir -p ~/ros2_ws/src/drone_delivery_interfaces/action
```

Create the ChangeDestination service:

```bash
cat > ~/ros2_ws/src/drone_delivery_interfaces/srv/ChangeDestination.srv << 'EOF'
# REQUEST — what ground control sends to the drone
float64 latitude
float64 longitude
string destination_name
---
# RESPONSE — what the drone sends back
bool success
string message
string previous_destination
EOF
```

### Step 3: Create Action Definition

```bash
cat > ~/ros2_ws/src/drone_delivery_interfaces/action/DeliverPackage.action << 'EOF'
# GOAL — what we want the drone to do
float64 target_latitude
float64 target_longitude
string package_id
string destination_name
float32 max_speed
---
# RESULT — final outcome when mission ends
bool success
string message
float32 delivery_time_seconds
float32 total_distance_km
---
# FEEDBACK — live updates during the mission
float32 progress_percent
string current_phase
float32 estimated_time_remaining
float64 current_latitude
float64 current_longitude
float32 battery_remaining
string status_message
EOF
```

### Step 4: Update CMakeLists.txt for Interfaces

```bash
cat > ~/ros2_ws/src/drone_delivery_interfaces/CMakeLists.txt << 'EOF'
cmake_minimum_required(VERSION 3.8)
project(drone_delivery_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find required packages
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

# Generate interfaces from .srv and .action files
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/ChangeDestination.srv"
  "action/DeliverPackage.action"
  DEPENDENCIES std_msgs
)

ament_package()
EOF
```

### Step 5: Update package.xml for Interfaces

```bash
cat > ~/ros2_ws/src/drone_delivery_interfaces/package.xml << 'EOF'
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd"
            schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>drone_delivery_interfaces</name>
  <version>1.0.0</version>
  <description>Custom ROS2 interfaces for the Drone Delivery System</description>
  <maintainer email="student@university.edu">Workshop Student</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>rosidl_default_generators</buildtool_depend>

  <depend>rosidl_default_runtime</depend>
  <depend>action_msgs</depend>
  <depend>std_msgs</depend>

  <member_of_group>rosidl_interface_packages</member_of_group>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
EOF
```

### Step 6: Build Interfaces Package First

```bash
cd ~/ros2_ws
colcon build --packages-select drone_delivery_interfaces
source install/setup.bash

# Verify interfaces were created
ros2 interface show drone_delivery_interfaces/srv/ChangeDestination
ros2 interface show drone_delivery_interfaces/action/DeliverPackage
```

**Expected output for the service:**
```
float64 latitude
float64 longitude
string destination_name
---
bool success
string message
string previous_destination
```

### Step 7: Create the Python Package

```bash
cd ~/ros2_ws/src

ros2 pkg create drone_delivery_system \
    --build-type ament_python \
    --dependencies rclpy std_msgs sensor_msgs std_srvs drone_delivery_interfaces
```

This creates:

```
drone_delivery_system/
├── drone_delivery_system/   ← Python module (your nodes go here)
│   └── __init__.py
├── resource/
│   └── drone_delivery_system
├── test/
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
├── package.xml
├── setup.cfg
└── setup.py
```

### Step 8: Add Launch Folder

```bash
mkdir -p ~/ros2_ws/src/drone_delivery_system/launch
```

### Step 9: Update package.xml for Main Package

```bash
cat > ~/ros2_ws/src/drone_delivery_system/package.xml << 'EOF'
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd"
            schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>drone_delivery_system</name>
  <version>1.0.0</version>
  <description>
    ROS2 Drone Delivery System — Complete Workshop Project.
    Students learn Nodes, Topics, Services, Actions, Parameters,
    and Launch Files through a realistic drone delivery simulation.
  </description>
  <maintainer email="student@university.edu">Workshop Student</maintainer>
  <license>Apache-2.0</license>

  <exec_depend>rclpy</exec_depend>
  <exec_depend>std_msgs</exec_depend>
  <exec_depend>sensor_msgs</exec_depend>
  <exec_depend>std_srvs</exec_depend>
  <exec_depend>drone_delivery_interfaces</exec_depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
EOF
```

### Step 10: Update setup.py

```bash
cat > ~/ros2_ws/src/drone_delivery_system/setup.py << 'EOF'
from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'drone_delivery_system'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # Required for ROS2 to find the package
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Workshop Student',
    maintainer_email='student@university.edu',
    description='ROS2 Drone Delivery System Workshop',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Format: 'executable_name = package.module:function'
            'drone_status_node = drone_delivery_system.drone_status_node:main',
            'battery_monitor_node = drone_delivery_system.battery_monitor_node:main',
            'gps_node = drone_delivery_system.gps_node:main',
            'ground_control_node = drone_delivery_system.ground_control_node:main',
            'takeoff_service_server = drone_delivery_system.takeoff_service_server:main',
            'takeoff_service_client = drone_delivery_system.takeoff_service_client:main',
            'destination_service_server = drone_delivery_system.destination_service_server:main',
            'destination_service_client = drone_delivery_system.destination_service_client:main',
            'delivery_action_server = drone_delivery_system.delivery_action_server:main',
            'delivery_action_client = drone_delivery_system.delivery_action_client:main',
        ],
    },
)
EOF
```

### Complete Folder Structure So Far

```
~/ros2_ws/
├── src/
│   ├── drone_delivery_interfaces/
│   │   ├── srv/
│   │   │   └── ChangeDestination.srv
│   │   ├── action/
│   │   │   └── DeliverPackage.action
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   │
│   └── drone_delivery_system/
│       ├── drone_delivery_system/
│       │   ├── __init__.py
│       │   ├── drone_status_node.py        ← PART 4
│       │   ├── battery_monitor_node.py     ← PART 4
│       │   ├── gps_node.py                 ← PART 4
│       │   ├── ground_control_node.py      ← PART 5
│       │   ├── takeoff_service_server.py   ← PART 6
│       │   ├── takeoff_service_client.py   ← PART 6
│       │   ├── destination_service_server.py ← PART 6
│       │   ├── destination_service_client.py ← PART 6
│       │   ├── delivery_action_server.py   ← PART 7
│       │   └── delivery_action_client.py   ← PART 7
│       ├── launch/
│       │   └── drone_delivery.launch.py    ← PART 9
│       ├── resource/
│       │   └── drone_delivery_system
│       ├── package.xml
│       ├── setup.cfg
│       └── setup.py
├── build/      (auto-generated)
├── install/    (auto-generated)
└── log/        (auto-generated)
```

---

# PART 4 — CREATE NODES

## What is a Node?

A node is a Python program that uses `rclpy` (the ROS2 Python client library). Every node:
1. Calls `rclpy.init()` — starts the ROS2 communication layer
2. Creates a `Node` object — registers with the ROS2 system
3. Does work (timers, publishers, subscribers)
4. Calls `rclpy.spin()` — keeps the program running and processing events
5. Calls `rclpy.shutdown()` — cleans up when done

## The ROS2 Node Lifecycle

```
rclpy.init()
    ↓
Create Node object (registers name, sets up comms)
    ↓
Create timers, publishers, subscribers, services
    ↓
rclpy.spin(node)  ← BLOCKS HERE — processes all callbacks
    ↓ (only exits on Ctrl+C or shutdown)
node.destroy_node()
    ↓
rclpy.shutdown()
```

---

## Node 1: Drone Status Node

**File:** `~/ros2_ws/src/drone_delivery_system/drone_delivery_system/drone_status_node.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/drone_delivery_system/drone_status_node.py << 'PYEOF'
#!/usr/bin/env python3
"""
Drone Status Node
================
Manages and publishes the operational state of the drone.

Valid States:
  IDLE        - Drone on ground, waiting for commands
  TAKING_OFF  - Drone ascending to cruise altitude
  FLYING      - Drone in transit to destination
  DELIVERING  - Drone lowering package at destination
  RETURNING   - Drone flying back to home base
  LANDING     - Drone descending to ground

Topics Published:
  /drone_status  (std_msgs/String)  — Current drone state

Topics Subscribed:
  /drone_state_command  (std_msgs/String)  — Commands to change state
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DroneStatusNode(Node):
    """Manages and publishes the drone's operational state."""

    # All valid drone states
    VALID_STATES = [
        'IDLE',
        'TAKING_OFF',
        'FLYING',
        'DELIVERING',
        'RETURNING',
        'LANDING'
    ]

    def __init__(self):
        # Call the parent Node constructor with our node name
        # This name is how other nodes identify us on the ROS2 network
        super().__init__('drone_status_node')

        # Initialize drone state
        self.current_state = 'IDLE'

        # --- PUBLISHER ---
        # Create a publisher on topic '/drone_status'
        # Message type: std_msgs/String
        # Queue size 10: buffer up to 10 messages before dropping old ones
        self.status_publisher = self.create_publisher(
            String,          # Message type
            '/drone_status', # Topic name
            10               # QoS queue size
        )

        # --- SUBSCRIBER ---
        # Listen for state change commands from other nodes
        self.state_subscriber = self.create_subscription(
            String,                    # Message type
            '/drone_state_command',    # Topic name
            self.state_command_callback,  # Function called when message arrives
            10                         # QoS queue size
        )

        # --- TIMER ---
        # Call publish_status() every 1.0 second
        # This keeps the status topic updated continuously
        self.timer = self.create_timer(1.0, self.publish_status)

        # Log startup messages
        self.get_logger().info('=' * 45)
        self.get_logger().info('  Drone Status Node — ONLINE')
        self.get_logger().info('=' * 45)
        self.get_logger().info(f'  Initial state : {self.current_state}')
        self.get_logger().info(f'  Publishing on : /drone_status')
        self.get_logger().info(f'  Listening on  : /drone_state_command')
        self.get_logger().info('=' * 45)

    def state_command_callback(self, msg):
        """
        Callback: Called automatically when a message arrives on /drone_state_command.
        'msg' is the received String message.
        'msg.data' contains the actual string value.
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
                f'Invalid state command: "{new_state}". '
                f'Valid states: {self.VALID_STATES}'
            )

    def publish_status(self):
        """
        Timer callback: Called every 1 second.
        Creates and publishes the drone status message.
        """
        msg = String()
        msg.data = self.current_state  # Set the string data

        self.status_publisher.publish(msg)
        self.get_logger().info(f'📡 Status: [{self.current_state}]')


def main(args=None):
    """
    Entry point for the node.
    All ROS2 Python nodes follow this exact pattern.
    """
    # Initialize the ROS2 communication system
    rclpy.init(args=args)

    # Create our node
    node = DroneStatusNode()

    # Keep the node running and processing callbacks
    # This blocks until Ctrl+C or rclpy.shutdown() is called
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Drone Status Node shutting down...')
    finally:
        # Always clean up properly
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
PYEOF
```

---

## Node 2: Battery Monitor Node

**File:** `~/ros2_ws/src/drone_delivery_system/drone_delivery_system/battery_monitor_node.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/drone_delivery_system/battery_monitor_node.py << 'PYEOF'
#!/usr/bin/env python3
"""
Battery Monitor Node
====================
Simulates drone battery and publishes percentage to /battery_status.

In a real drone this node would read from the battery management system (BMS)
via a hardware interface (serial, I2C, CAN bus).

Topics Published:
  /battery_status  (std_msgs/Float32)  — Battery percentage 0.0-100.0

Parameters:
  battery_warning_threshold  (float, default: 20.0) — Warn below this %
  initial_battery            (float, default: 100.0) — Starting charge
  discharge_rate             (float, default: 0.5)   — % lost per second
"""

import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class BatteryMonitorNode(Node):
    """Simulates and publishes drone battery percentage."""

    def __init__(self):
        super().__init__('battery_monitor_node')

        # --- DECLARE PARAMETERS ---
        # Parameters allow values to be set at launch or changed at runtime
        # Format: declare_parameter('name', default_value)
        self.declare_parameter('battery_warning_threshold', 20.0)
        self.declare_parameter('initial_battery', 100.0)
        self.declare_parameter('discharge_rate', 0.5)

        # --- READ PARAMETERS ---
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

        # --- PUBLISHER ---
        self.battery_publisher = self.create_publisher(
            Float32,           # Floating point number message
            '/battery_status', # Topic name
            10
        )

        # --- TIMER ---
        # Publish battery every 2 seconds
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
        Timer callback: Simulate discharge and publish battery level.
        Called every 2 seconds by the timer.
        """
        # Re-read discharge_rate in case it was changed with ros2 param set
        self.discharge_rate = (
            self.get_parameter('discharge_rate')
            .get_parameter_value().double_value
        )

        # Simulate battery discharge (2 seconds passed × discharge_rate)
        self.battery_level -= self.discharge_rate * 2.0
        self.battery_level = max(0.0, self.battery_level)  # Floor at 0%

        # Add small random noise to simulate real sensor readings
        noise = random.uniform(-0.2, 0.2)
        display_level = max(0.0, min(100.0, self.battery_level + noise))

        # --- BUILD AND PUBLISH MESSAGE ---
        msg = Float32()
        msg.data = display_level
        self.battery_publisher.publish(msg)

        # Log with visual battery indicator
        bar = self._battery_bar(display_level)
        if display_level <= self.warning_threshold:
            self.get_logger().warn(
                f'🔴 LOW BATTERY! {display_level:.1f}% {bar} ← RTH Recommended!'
            )
        elif display_level <= 50.0:
            self.get_logger().warn(
                f'🟡 Battery: {display_level:.1f}% {bar}'
            )
        else:
            self.get_logger().info(
                f'🟢 Battery: {display_level:.1f}% {bar}'
            )

    def _battery_bar(self, level):
        """Create a visual battery bar indicator."""
        filled = int(level / 10)
        empty = 10 - filled
        return f'[{"█" * filled}{"░" * empty}]'


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
PYEOF
```

---

## Node 3: GPS Node

**File:** `~/ros2_ws/src/drone_delivery_system/drone_delivery_system/gps_node.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/drone_delivery_system/gps_node.py << 'PYEOF'
#!/usr/bin/env python3
"""
GPS Node
========
Simulates GPS receiver and publishes coordinates to /gps_location.

Uses sensor_msgs/NavSatFix — the standard ROS2 GPS message format.
This exact message type is used by real GPS hardware drivers (ublox, Garmin, etc.)
so switching from simulation to real hardware requires NO code changes here.

In a real drone:
  - This node reads from a serial/USB GPS module
  - Or bridges from MAVLink (PX4/ArduPilot) via MAVROS

Topics Published:
  /gps_location  (sensor_msgs/NavSatFix)  — GPS coordinates

Parameters:
  home_latitude   (float, default: 23.5880) — Base latitude
  home_longitude  (float, default: 58.3829) — Base longitude
  home_altitude   (float, default: 50.0)    — Altitude in meters
"""

import math
import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix, NavSatStatus


class GPSNode(Node):
    """Simulates a GPS receiver and publishes location data."""

    def __init__(self):
        super().__init__('gps_node')

        # Declare parameters (defaulting to Muscat, Oman coordinates)
        self.declare_parameter('home_latitude', 23.5880)
        self.declare_parameter('home_longitude', 58.3829)
        self.declare_parameter('home_altitude', 50.0)

        # Read parameters
        self.home_lat = (
            self.get_parameter('home_latitude')
            .get_parameter_value().double_value
        )
        self.home_lon = (
            self.get_parameter('home_longitude')
            .get_parameter_value().double_value
        )
        self.home_alt = (
            self.get_parameter('home_altitude')
            .get_parameter_value().double_value
        )

        # Current position (starts at home)
        self.current_lat = self.home_lat
        self.current_lon = self.home_lon
        self.current_alt = self.home_alt

        # Track time for simulated movement
        self.start_time = time.time()

        # --- PUBLISHER ---
        # NavSatFix is the standard GPS message in ROS2/ROS
        # It contains: latitude, longitude, altitude, covariance, status
        self.gps_publisher = self.create_publisher(
            NavSatFix,        # Standard GPS message type
            '/gps_location',  # Topic name (matches what subscribers expect)
            10
        )

        # --- TIMER ---
        # Real GPS receivers typically output at 1-10 Hz
        self.timer = self.create_timer(1.0, self.publish_gps)

        self.get_logger().info('=' * 45)
        self.get_logger().info('  GPS Node — ONLINE')
        self.get_logger().info('=' * 45)
        self.get_logger().info(f'  Home: {self.home_lat:.6f}°N, {self.home_lon:.6f}°E')
        self.get_logger().info(f'  Altitude: {self.home_alt:.1f} m')
        self.get_logger().info('=' * 45)

    def publish_gps(self):
        """
        Timer callback: Simulate GPS movement and publish coordinates.
        Simulates a slow circular drift around home position.
        """
        elapsed = time.time() - self.start_time

        # Simulate slight GPS drift (circular motion around home)
        drift_radius = 0.00005  # ~5.5 meters in degrees
        lat_offset = drift_radius * math.sin(elapsed * 0.05)
        lon_offset = drift_radius * math.cos(elapsed * 0.05)

        # Build the NavSatFix message
        msg = NavSatFix()

        # Header: timestamp and coordinate frame
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'gps_frame'

        # GPS Status
        msg.status.status = NavSatStatus.STATUS_FIX      # Has GPS fix
        msg.status.service = NavSatStatus.SERVICE_GPS     # Using GPS

        # Position
        msg.latitude = self.current_lat + lat_offset
        msg.longitude = self.current_lon + lon_offset
        msg.altitude = self.current_alt

        # Position covariance (uncertainty in meters²)
        # Diagonal entries: [lat_var, lon_var, alt_var, ...]
        msg.position_covariance = [
            0.1, 0.0, 0.0,
            0.0, 0.1, 0.0,
            0.0, 0.0, 0.5
        ]
        msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN

        self.gps_publisher.publish(msg)

        self.get_logger().info(
            f'📍 GPS: {msg.latitude:.6f}°N, '
            f'{msg.longitude:.6f}°E, '
            f'Alt: {msg.altitude:.1f}m'
        )

    def update_position(self, lat, lon, alt=None):
        """Update the simulated drone position (called by delivery action)."""
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
PYEOF
```

---

## Build and Test the Nodes

```bash
cd ~/ros2_ws
colcon build --packages-select drone_delivery_system
source install/setup.bash
```

**Expected output:**
```
Starting >>> drone_delivery_system
Finished <<< drone_delivery_system [3.2s]

Summary: 1 package finished [3.4s]
```

### Run Each Node (in separate terminals)

**Terminal 1:**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run drone_delivery_system drone_status_node
```
Output:
```
[INFO] [drone_status_node]: =============================================
[INFO] [drone_status_node]:   Drone Status Node — ONLINE
[INFO] [drone_status_node]:   Initial state : IDLE
[INFO] [drone_status_node]: 📡 Status: [IDLE]
[INFO] [drone_status_node]: 📡 Status: [IDLE]
```

**Terminal 2:**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run drone_delivery_system battery_monitor_node
```
Output:
```
[INFO] [battery_monitor_node]:   Battery Monitor Node — ONLINE
[INFO] [battery_monitor_node]:   Initial charge  : 100.0%
[INFO] [battery_monitor_node]: 🟢 Battery: 99.0% [██████████]
[INFO] [battery_monitor_node]: 🟢 Battery: 98.0% [█████████░]
```

**Terminal 3:**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run drone_delivery_system gps_node
```
Output:
```
[INFO] [gps_node]:   GPS Node — ONLINE
[INFO] [gps_node]:   Home: 23.588000°N, 58.382900°E
[INFO] [gps_node]: 📍 GPS: 23.588005°N, 58.382900°E, Alt: 50.0m
```

### Inspect Nodes (Terminal 4)

```bash
# List all running nodes
ros2 node list
```
Output:
```
/battery_monitor_node
/drone_status_node
/gps_node
```

```bash
# Get detailed info about a node
ros2 node info /battery_monitor_node
```
Output:
```
/battery_monitor_node
  Subscribers: (none)
  Publishers:
    /battery_status: std_msgs/msg/Float32
    /rosout: rcl_interfaces/msg/Log
  Service Servers: (none)
  Service Clients: (none)
  Action Servers: (none)
  Action Clients: (none)
```

---

# PART 5 — TOPICS (PUBLISHER / SUBSCRIBER)

## Why Topics?

Topics provide **asynchronous, decoupled communication**. The publisher doesn't know who is listening. The subscriber doesn't know who is publishing. They just communicate through the topic name.

```
Real drone analogy:
A drone's flight controller broadcasts telemetry on a radio frequency (topic).
Ground station radios tuned to that frequency receive it (subscribe).
Both sides don't need to know about each other.
```

## Ground Control Node — The Full Telemetry Dashboard

**File:** `~/ros2_ws/src/drone_delivery_system/drone_delivery_system/ground_control_node.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/drone_delivery_system/ground_control_node.py << 'PYEOF'
#!/usr/bin/env python3
"""
Ground Control Node
===================
The nerve center of the drone delivery system.
Subscribes to ALL telemetry topics and displays a live dashboard.

In a real system, this would also display a map, flight path visualization,
video feed, and have buttons/controls for the operator.

Topics Subscribed:
  /battery_status  (std_msgs/Float32)    — Battery percentage
  /gps_location    (sensor_msgs/NavSatFix)  — GPS coordinates
  /drone_status    (std_msgs/String)     — Operational state

This demonstrates:
  - Multiple subscribers in one node
  - Storing received data and displaying it periodically
  - Combining data from different topics
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from sensor_msgs.msg import NavSatFix


class GroundControlNode(Node):
    """Ground control station — monitors all drone telemetry."""

    def __init__(self):
        super().__init__('ground_control_node')

        # Storage for latest telemetry data
        # These start as None until the first message arrives
        self.battery_level = None
        self.gps_data = None
        self.drone_status = None
        self.messages_received = {'battery': 0, 'gps': 0, 'status': 0}

        # ======================================================
        # SUBSCRIBER 1: Battery Status
        # ======================================================
        self.battery_sub = self.create_subscription(
            Float32,
            '/battery_status',
            self.battery_callback,  # Called when battery message arrives
            10
        )

        # ======================================================
        # SUBSCRIBER 2: GPS Location
        # ======================================================
        self.gps_sub = self.create_subscription(
            NavSatFix,
            '/gps_location',
            self.gps_callback,      # Called when GPS message arrives
            10
        )

        # ======================================================
        # SUBSCRIBER 3: Drone Status
        # ======================================================
        self.status_sub = self.create_subscription(
            String,
            '/drone_status',
            self.status_callback,   # Called when status message arrives
            10
        )

        # ======================================================
        # TIMER: Display dashboard every 3 seconds
        # ======================================================
        self.timer = self.create_timer(3.0, self.display_dashboard)

        self.get_logger().info('🛰️  Ground Control Station — ONLINE')
        self.get_logger().info('   Monitoring: /battery_status, /gps_location, /drone_status')
        self.get_logger().info('   Waiting for drone telemetry...')

    # ===========================================================
    # CALLBACK FUNCTIONS
    # Each callback runs AUTOMATICALLY when a message arrives
    # They store the data for the dashboard to display
    # ===========================================================

    def battery_callback(self, msg):
        """Called automatically every time a battery message arrives."""
        # msg.data is the float32 battery percentage value
        self.battery_level = msg.data
        self.messages_received['battery'] += 1

    def gps_callback(self, msg):
        """Called automatically every time a GPS message arrives."""
        # msg contains latitude, longitude, altitude, status, etc.
        self.gps_data = msg
        self.messages_received['gps'] += 1

    def status_callback(self, msg):
        """Called automatically every time a status message arrives."""
        # msg.data is the string state name
        self.drone_status = msg.data
        self.messages_received['status'] += 1

    def display_dashboard(self):
        """Timer callback: Display formatted telemetry dashboard."""
        separator = '─' * 50
        self.get_logger().info('\n' + '═' * 50)
        self.get_logger().info('         🚁  GROUND CONTROL DASHBOARD  🚁')
        self.get_logger().info('═' * 50)

        # --- Drone Status ---
        if self.drone_status:
            state_emoji = {
                'IDLE': '⏸️ ', 'TAKING_OFF': '🚀', 'FLYING': '✈️ ',
                'DELIVERING': '📦', 'RETURNING': '🔄', 'LANDING': '🛬'
            }.get(self.drone_status, '❓')
            self.get_logger().info(
                f'  {state_emoji} Status    : {self.drone_status}'
            )
        else:
            self.get_logger().info('  ❓ Status    : No signal...')

        # --- Battery ---
        if self.battery_level is not None:
            bar = self._battery_bar(self.battery_level)
            status_str = '⚠️ LOW' if self.battery_level < 20 else '✅ OK'
            self.get_logger().info(
                f'  🔋 Battery   : {self.battery_level:.1f}% {bar} {status_str}'
            )
        else:
            self.get_logger().info('  🔋 Battery   : No signal...')

        # --- GPS ---
        if self.gps_data:
            self.get_logger().info(
                f'  📍 GPS Lat   : {self.gps_data.latitude:.6f}°'
            )
            self.get_logger().info(
                f'  📍 GPS Lon   : {self.gps_data.longitude:.6f}°'
            )
            self.get_logger().info(
                f'  🏔️  Altitude  : {self.gps_data.altitude:.1f} m'
            )
        else:
            self.get_logger().info('  📍 GPS       : No signal...')

        # --- Message counts ---
        self.get_logger().info(separator)
        self.get_logger().info(
            f'  📊 Msgs rx   : '
            f'Battery={self.messages_received["battery"]} | '
            f'GPS={self.messages_received["gps"]} | '
            f'Status={self.messages_received["status"]}'
        )
        self.get_logger().info('═' * 50)

    def _battery_bar(self, level):
        """Create ASCII battery bar visualization."""
        filled = int(level / 10)
        empty = 10 - filled
        return f'[{"█" * filled}{"░" * empty}]'


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
PYEOF
```

## Build and Test Topics

```bash
cd ~/ros2_ws
colcon build --packages-select drone_delivery_system
source install/setup.bash
```

Run in 4 separate terminals:

**Terminal 1:** `ros2 run drone_delivery_system drone_status_node`
**Terminal 2:** `ros2 run drone_delivery_system battery_monitor_node`
**Terminal 3:** `ros2 run drone_delivery_system gps_node`
**Terminal 4:** `ros2 run drone_delivery_system ground_control_node`

### Essential Topic Commands

```bash
# List all active topics
ros2 topic list
```
Output:
```
/battery_status
/drone_state_command
/drone_status
/gps_location
/parameter_events
/rosout
```

```bash
# See live messages on a topic
ros2 topic echo /battery_status
```
Output:
```
data: 87.4299...
---
data: 86.4299...
---
```

```bash
# See GPS data (more complex message)
ros2 topic echo /gps_location
```
Output:
```
header:
  stamp:
    sec: 1704067200
    nanosec: 123456789
  frame_id: gps_frame
status:
  status: 0
  service: 1
latitude: 23.588005234
longitude: 58.382900123
altitude: 50.0
```

```bash
# Check publish frequency (should be ~0.5 Hz for battery, 1.0 Hz for GPS)
ros2 topic hz /battery_status
```
Output:
```
average rate: 0.500
   min: 1.993s  max: 2.007s  std dev: 0.004s  window: 5
```

```bash
# Check message type and connections
ros2 topic info /gps_location
```
Output:
```
Type: sensor_msgs/msg/NavSatFix
Publisher count: 1
Subscription count: 1
```

```bash
# See the message field structure
ros2 interface show sensor_msgs/msg/NavSatFix
```

---

# PART 6 — SERVICES

## Why Services?

Services are **synchronous request/response** communication. Unlike topics (fire-and-forget), services guarantee you get an answer.

```
Topic:   Drone --publishes battery--> [nobody has to listen]
Service: Ground --"takeoff?"--> Drone --"confirmed"--> Ground
```

Services are perfect for:
- Commands that need confirmation
- Queries that need answers
- One-shot operations

## Service Server 1: Takeoff and Land

**File:** `~/ros2_ws/src/drone_delivery_system/drone_delivery_system/takeoff_service_server.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/drone_delivery_system/takeoff_service_server.py << 'PYEOF'
#!/usr/bin/env python3
"""
Takeoff / Land Service Server
==============================
Provides two services:
  /takeoff  (std_srvs/Trigger) — Command drone to take off
  /land     (std_srvs/Trigger) — Command drone to land

std_srvs/Trigger is a simple built-in service:
  REQUEST:  (empty — just send the call)
  RESPONSE: bool success
            string message

Services Provided:
  /takeoff  (std_srvs/Trigger)
  /land     (std_srvs/Trigger)
"""

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from std_msgs.msg import String


class TakeoffServiceServer(Node):
    """Handles takeoff and landing commands."""

    def __init__(self):
        super().__init__('takeoff_service_server')

        # Track drone state
        self.is_airborne = False
        self.current_altitude = 0.0
        self.target_altitude = 50.0

        # Publisher to update drone status
        self.state_pub = self.create_publisher(String, '/drone_state_command', 10)

        # ======================================================
        # SERVICE SERVER 1: /takeoff
        # ======================================================
        # create_service(type, name, callback_function)
        self.takeoff_srv = self.create_service(
            Trigger,               # Service message type
            '/takeoff',            # Service name
            self.takeoff_callback  # Function called when service is requested
        )

        # ======================================================
        # SERVICE SERVER 2: /land
        # ======================================================
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
        Called when a client calls the /takeoff service.

        Parameters:
          request  - The service request (Trigger.Request — empty)
          response - The response to fill and return (Trigger.Response)

        Returns:
          response - Modified response with success and message
        """
        if self.is_airborne:
            # Cannot take off if already flying
            response.success = False
            response.message = (
                '❌ REJECTED: Drone is already airborne at '
                f'{self.current_altitude:.1f}m. '
                'Land first before taking off again.'
            )
            self.get_logger().warn('Takeoff rejected — already airborne')
        else:
            # Execute takeoff
            self.is_airborne = True
            self.current_altitude = self.target_altitude

            response.success = True
            response.message = (
                f'✅ TAKEOFF CONFIRMED: Drone ascending to {self.target_altitude}m. '
                'All pre-flight checks passed. Propellers spinning.'
            )

            # Publish state change
            self._publish_state('TAKING_OFF')
            self.get_logger().info(f'🚀 TAKEOFF! Ascending to {self.target_altitude}m')

        return response  # MUST return the response

    def land_callback(self, request, response):
        """Called when a client calls the /land service."""
        if not self.is_airborne:
            response.success = False
            response.message = (
                '❌ REJECTED: Drone is already on the ground. '
                'Cannot land what is not flying.'
            )
            self.get_logger().warn('Land rejected — already on ground')
        else:
            # Execute landing
            self.is_airborne = False
            self.current_altitude = 0.0

            response.success = True
            response.message = (
                '✅ LANDING CONFIRMED: Initiating descent sequence. '
                'Estimated touchdown in 30 seconds.'
            )

            self._publish_state('LANDING')
            self.get_logger().info('🛬 LANDING! Descending to ground...')

        return response

    def _publish_state(self, state):
        """Helper to publish a state change command."""
        msg = String()
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
PYEOF
```

## Service Client 1: Takeoff Client

**File:** `~/ros2_ws/src/drone_delivery_system/drone_delivery_system/takeoff_service_client.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/drone_delivery_system/takeoff_service_client.py << 'PYEOF'
#!/usr/bin/env python3
"""
Takeoff Service Client
======================
Sends takeoff or landing commands to the drone service server.

Usage:
  ros2 run drone_delivery_system takeoff_service_client           # Takeoff
  ros2 run drone_delivery_system takeoff_service_client land      # Land
"""

import sys
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class TakeoffServiceClient(Node):
    """Client that sends takeoff/land commands to the drone."""

    def __init__(self):
        super().__init__('takeoff_service_client')

        # Create service clients
        # These are CLIENTS — they CALL services, not provide them
        self.takeoff_client = self.create_client(Trigger, '/takeoff')
        self.land_client = self.create_client(Trigger, '/land')

    def send_takeoff(self):
        """Send a takeoff command and wait for response."""
        self.get_logger().info('📡 Sending TAKEOFF command...')

        # Wait until the service is available (up to 5 seconds)
        if not self.takeoff_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error(
                '❌ /takeoff service not available! Is the server running?'
            )
            return None

        # Create the request (empty for Trigger)
        request = Trigger.Request()

        # Call the service ASYNCHRONOUSLY (returns a Future)
        future = self.takeoff_client.call_async(request)

        # Wait for the future to complete (blocks until response received)
        rclpy.spin_until_future_complete(self, future)

        # Get the result
        response = future.result()

        # Display the response
        if response.success:
            self.get_logger().info(f'✅ Response: {response.message}')
        else:
            self.get_logger().error(f'❌ Response: {response.message}')

        return response

    def send_land(self):
        """Send a landing command and wait for response."""
        self.get_logger().info('📡 Sending LAND command...')

        if not self.land_client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('❌ /land service not available!')
            return None

        request = Trigger.Request()
        future = self.land_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        response = future.result()

        if response.success:
            self.get_logger().info(f'✅ Response: {response.message}')
        else:
            self.get_logger().error(f'❌ Response: {response.message}')

        return response


def main(args=None):
    rclpy.init(args=args)
    client = TakeoffServiceClient()

    # Check command line argument
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'land':
        client.send_land()
    else:
        client.send_takeoff()

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
PYEOF
```

## Service Server 2: Destination Change

**File:** `~/ros2_ws/src/drone_delivery_system/drone_delivery_system/destination_service_server.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/drone_delivery_system/destination_service_server.py << 'PYEOF'
#!/usr/bin/env python3
"""
Destination Service Server
==========================
Allows ground control to update the delivery destination in real-time.
Uses our custom ChangeDestination service type.

Services Provided:
  /change_destination  (drone_delivery_interfaces/ChangeDestination)
"""

import rclpy
from rclpy.node import Node
from drone_delivery_interfaces.srv import ChangeDestination


class DestinationServiceServer(Node):
    """Manages delivery destination updates."""

    # Known delivery locations in Muscat, Oman
    KNOWN_LOCATIONS = {
        'Home Base': (23.5880, 58.3829),
        'Sultan Qaboos University': (23.6097, 58.1804),
        'Muscat City Centre': (23.5957, 58.2772),
        'Royal Opera House': (23.6134, 58.5928),
        'Muttrah Corniche': (23.6177, 58.5902),
    }

    def __init__(self):
        super().__init__('destination_service_server')

        # Current delivery destination
        self.current_destination = {
            'name': 'Home Base',
            'latitude': 23.5880,
            'longitude': 58.3829
        }

        # Create service server
        self.srv = self.create_service(
            ChangeDestination,         # Our CUSTOM service type
            '/change_destination',     # Service name
            self.change_destination_callback
        )

        self.get_logger().info('=' * 50)
        self.get_logger().info('  Destination Service Server — READY')
        self.get_logger().info('=' * 50)
        self.get_logger().info(
            f'  Current: {self.current_destination["name"]}'
        )
        self.get_logger().info('  Known locations:')
        for name, coords in self.KNOWN_LOCATIONS.items():
            self.get_logger().info(f'    • {name}: {coords[0]:.4f}, {coords[1]:.4f}')
        self.get_logger().info('=' * 50)

    def change_destination_callback(self, request, response):
        """
        Called when a client requests to change the delivery destination.

        Request fields:
          request.latitude         - Target latitude
          request.longitude        - Target longitude
          request.destination_name - Human-readable location name

        Response fields:
          response.success              - Whether the change succeeded
          response.message              - Confirmation or error message
          response.previous_destination - What the old destination was
        """
        # Save the previous destination name for the response
        previous = self.current_destination['name']

        # Validate coordinates
        if not (-90 <= request.latitude <= 90):
            response.success = False
            response.message = f'❌ Invalid latitude: {request.latitude}'
            response.previous_destination = previous
            return response

        if not (-180 <= request.longitude <= 180):
            response.success = False
            response.message = f'❌ Invalid longitude: {request.longitude}'
            response.previous_destination = previous
            return response

        # Calculate distance from current position
        distance = self._simple_distance(
            self.current_destination['latitude'],
            self.current_destination['longitude'],
            request.latitude,
            request.longitude
        )

        # Update destination
        self.current_destination = {
            'name': request.destination_name,
            'latitude': request.latitude,
            'longitude': request.longitude
        }

        # Fill response
        response.success = True
        response.previous_destination = previous
        response.message = (
            f'✅ Destination updated!\n'
            f'   Previous: {previous}\n'
            f'   New:      {request.destination_name}\n'
            f'   Coords:   ({request.latitude:.4f}°N, {request.longitude:.4f}°E)\n'
            f'   Distance: ~{distance:.1f} km from previous'
        )

        self.get_logger().info(
            f'📍 Destination: {previous} → {request.destination_name}'
        )

        return response

    def _simple_distance(self, lat1, lon1, lat2, lon2):
        """Rough distance calculation in km."""
        dlat = abs(lat2 - lat1) * 111.0  # 1 degree lat ≈ 111 km
        dlon = abs(lon2 - lon1) * 111.0 * 0.85  # Adjust for Oman latitude
        return (dlat**2 + dlon**2)**0.5


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
PYEOF
```

## Service Client 2: Destination Client

**File:** `~/ros2_ws/src/drone_delivery_system/drone_delivery_system/destination_service_client.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/drone_delivery_system/destination_service_client.py << 'PYEOF'
#!/usr/bin/env python3
"""
Destination Service Client
==========================
Changes the drone's delivery destination.

Usage:
  ros2 run drone_delivery_system destination_service_client
  # Or via command line:
  ros2 service call /change_destination drone_delivery_interfaces/srv/ChangeDestination
    "{latitude: 23.6097, longitude: 58.1804, destination_name: 'SQU'}"
"""

import rclpy
from rclpy.node import Node
from drone_delivery_interfaces.srv import ChangeDestination


class DestinationServiceClient(Node):
    """Client to change the delivery destination."""

    def __init__(self):
        super().__init__('destination_service_client')

        self.client = self.create_client(
            ChangeDestination,
            '/change_destination'
        )

    def change_destination(self, name, latitude, longitude):
        """Send a destination change request."""
        self.get_logger().info(f'📡 Changing destination to: {name}')

        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('❌ /change_destination service not available!')
            return None

        # Build the custom request
        request = ChangeDestination.Request()
        request.destination_name = name
        request.latitude = latitude
        request.longitude = longitude

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
        longitude=58.1804
    )

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
PYEOF
```

## Build and Test Services

```bash
cd ~/ros2_ws
colcon build --packages-select drone_delivery_system
source install/setup.bash
```

**Terminal 1:** Run the service servers:
```bash
ros2 run drone_delivery_system takeoff_service_server
```

**Terminal 2:** Test takeoff:
```bash
ros2 run drone_delivery_system takeoff_service_client
```
Output:
```
[INFO] [takeoff_service_client]: 📡 Sending TAKEOFF command...
[INFO] [takeoff_service_client]: ✅ Response: TAKEOFF CONFIRMED: Drone ascending to 50.0m...
```

**Terminal 3:** Or test directly with ros2 CLI (no client code needed!):
```bash
ros2 service call /takeoff std_srvs/srv/Trigger {}
```
Output:
```
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(success=True, message='✅ TAKEOFF CONFIRMED...')
```

```bash
# List all services
ros2 service list
```
Output:
```
/change_destination
/land
/takeoff
/battery_monitor_node/describe_parameters
/battery_monitor_node/get_parameters
...
```

```bash
# Show service interface
ros2 interface show drone_delivery_interfaces/srv/ChangeDestination
```
Output:
```
float64 latitude
float64 longitude
string destination_name
---
bool success
string message
string previous_destination
```

```bash
# Call custom service via CLI
ros2 service call /change_destination \
  drone_delivery_interfaces/srv/ChangeDestination \
  "{latitude: 23.6097, longitude: 58.1804, destination_name: 'SQU'}"
```

---

# PART 7 — ACTIONS

## Why Actions?

Actions are for **long-running tasks** that need:
1. A way to send a **goal** (start the task)
2. **Ongoing feedback** (progress updates)
3. A **final result** (succeeded/failed)
4. The ability to **cancel** the task mid-way

```
Service: "Take off" → immediate response
Action:  "Deliver to SQU" → takes 30 minutes, need updates every 10 seconds

Without actions, you'd need to:
  - Poll with services every 10 seconds (wasteful, fragile)
  - Create custom topic + service combos (complex, not standard)
  - Actions give you ALL of this in one clean pattern
```

## Delivery Action Server

**File:** `~/ros2_ws/src/drone_delivery_system/drone_delivery_system/delivery_action_server.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/drone_delivery_system/delivery_action_server.py << 'PYEOF'
#!/usr/bin/env python3
"""
Delivery Action Server
======================
Manages complete drone delivery missions from takeoff to landing.

Mission Phases (with progress %):
  Phase 1: TAKEOFF          (0%  → 10%)
  Phase 2: FLY_TO_DEST      (10% → 50%)
  Phase 3: DELIVERING       (50% → 70%)
  Phase 4: RETURN_HOME      (70% → 95%)
  Phase 5: LANDING          (95% → 100%)

Actions Provided:
  /deliver_package  (drone_delivery_interfaces/DeliverPackage)

Features demonstrated:
  - ActionServer setup
  - Goal acceptance/rejection
  - Cancel handling
  - Continuous feedback publishing
  - Final result returning
"""

import time
import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
from drone_delivery_interfaces.action import DeliverPackage


class DeliveryActionServer(Node):
    """Action server for complete drone delivery missions."""

    def __init__(self):
        super().__init__('delivery_action_server')

        # Home base (Muscat, Oman)
        self.home_latitude = 23.5880
        self.home_longitude = 58.3829

        # Declare parameters
        self.declare_parameter('drone_speed_ms', 15.0)
        self.declare_parameter('max_altitude', 120.0)
        self.declare_parameter('delivery_hover_time', 10.0)

        self.drone_speed = (
            self.get_parameter('drone_speed_ms')
            .get_parameter_value().double_value
        )

        # Use ReentrantCallbackGroup to allow multiple simultaneous callbacks
        # This is needed when the action server needs to process cancel requests
        # while the execute callback is running
        self.callback_group = ReentrantCallbackGroup()

        # ======================================================
        # ACTION SERVER
        # ======================================================
        self._action_server = ActionServer(
            self,
            DeliverPackage,          # Action type
            '/deliver_package',       # Action name
            execute_callback=self.execute_callback,  # Main mission logic
            goal_callback=self.goal_callback,        # Accept/reject goals
            cancel_callback=self.cancel_callback,    # Accept/reject cancels
            callback_group=self.callback_group
        )

        # Publisher for state updates
        self.state_pub = self.create_publisher(
            String, '/drone_state_command', 10
        )

        self.get_logger().info('=' * 50)
        self.get_logger().info('  Delivery Action Server — READY')
        self.get_logger().info('  Action: /deliver_package')
        self.get_logger().info(f'  Speed:  {self.drone_speed} m/s')
        self.get_logger().info('  Waiting for delivery missions...')
        self.get_logger().info('=' * 50)

    # ==========================================================
    # GOAL CALLBACK
    # Called BEFORE accepting a goal — decide if you can do it
    # ==========================================================
    def goal_callback(self, goal_request):
        """
        Decide whether to accept or reject an incoming goal.
        Return GoalResponse.ACCEPT or GoalResponse.REJECT.
        """
        self.get_logger().info(
            f'📦 New delivery goal received!\n'
            f'   Package ID  : {goal_request.package_id}\n'
            f'   Destination : {goal_request.destination_name}\n'
            f'   Target      : ({goal_request.target_latitude:.4f}, '
            f'{goal_request.target_longitude:.4f})'
        )

        # Add validation logic here (e.g., check battery, airspace, etc.)
        # For this workshop, we accept all goals
        return GoalResponse.ACCEPT

    # ==========================================================
    # CANCEL CALLBACK
    # Called when client requests cancellation
    # ==========================================================
    def cancel_callback(self, goal_handle):
        """
        Decide whether to accept a cancel request.
        Return CancelResponse.ACCEPT or CancelResponse.REJECT.
        """
        self.get_logger().warn(
            f'⚠️  Cancel requested for package: {goal_handle.request.package_id}'
        )
        # Accept all cancel requests (you could reject during critical phases)
        return CancelResponse.ACCEPT

    # ==========================================================
    # EXECUTE CALLBACK
    # The main mission logic — runs in a separate thread
    # ==========================================================
    def execute_callback(self, goal_handle):
        """
        Execute the complete delivery mission.
        This function runs the entire mission and returns a Result when done.

        goal_handle provides:
          - goal_handle.request      : The original goal
          - goal_handle.is_cancel_requested : True if cancel was requested
          - goal_handle.publish_feedback(msg) : Send progress update
          - goal_handle.succeed()    : Mark as succeeded
          - goal_handle.canceled()   : Mark as canceled
          - goal_handle.abort()      : Mark as failed
        """
        goal = goal_handle.request
        self.get_logger().info(
            f'🚀 Mission started: {goal.package_id} → {goal.destination_name}'
        )

        # Pre-calculate mission parameters
        distance_km = self._haversine_distance(
            self.home_latitude, self.home_longitude,
            goal.target_latitude, goal.target_longitude
        )
        mission_start_time = time.time()
        initial_battery = 100.0
        battery_drain_per_km = 3.0  # % per km (simplified)

        # Create the feedback message object (reuse it, just update fields)
        feedback = DeliverPackage.Feedback()

        # ──────────────────────────────────────────────────────
        # PHASE 1: TAKEOFF (0% → 10%)
        # ──────────────────────────────────────────────────────
        self._publish_state('TAKING_OFF')
        self.get_logger().info('📍 Phase 1: TAKEOFF')

        for step in range(11):  # 0 to 10
            # Check for cancel request between each step
            if goal_handle.is_cancel_requested:
                self._publish_state('LANDING')
                goal_handle.canceled()
                self.get_logger().warn('Mission CANCELLED during takeoff')
                return self._make_result(False, 'Cancelled during takeoff', 0, 0)

            altitude = step * 5  # 0 to 50 meters
            elapsed = time.time() - mission_start_time
            battery = initial_battery - (elapsed * 0.1)

            feedback.progress_percent = float(step)
            feedback.current_phase = 'TAKEOFF'
            feedback.status_message = f'Ascending... {altitude}m / 50m'
            feedback.current_latitude = self.home_latitude
            feedback.current_longitude = self.home_longitude
            feedback.battery_remaining = battery
            feedback.estimated_time_remaining = (distance_km * 2 / self.drone_speed) * 1000

            goal_handle.publish_feedback(feedback)
            self.get_logger().info(
                f'  ↑ Altitude: {altitude}m | Battery: {battery:.1f}%'
            )
            time.sleep(0.4)

        # ──────────────────────────────────────────────────────
        # PHASE 2: FLY TO DESTINATION (10% → 50%)
        # ──────────────────────────────────────────────────────
        self._publish_state('FLYING')
        self.get_logger().info(
            f'📍 Phase 2: FLYING TO {goal.destination_name} ({distance_km:.2f} km)'
        )

        steps = 40
        for step in range(steps + 1):
            if goal_handle.is_cancel_requested:
                self._publish_state('RETURNING')
                goal_handle.canceled()
                self.get_logger().warn('Mission CANCELLED during flight')
                return self._make_result(False, 'Cancelled during flight', 0, 0)

            ratio = step / steps
            progress = 10.0 + (ratio * 40.0)
            elapsed = time.time() - mission_start_time
            battery = initial_battery - (distance_km * battery_drain_per_km * ratio) - (elapsed * 0.05)

            # Interpolate position between home and destination
            current_lat = (self.home_latitude +
                           (goal.target_latitude - self.home_latitude) * ratio)
            current_lon = (self.home_longitude +
                           (goal.target_longitude - self.home_longitude) * ratio)

            remaining_km = distance_km * (1 - ratio)
            eta_seconds = (remaining_km * 1000) / self.drone_speed

            feedback.progress_percent = progress
            feedback.current_phase = 'FLYING_TO_DESTINATION'
            feedback.status_message = f'En route to {goal.destination_name} — {remaining_km:.1f}km remaining'
            feedback.current_latitude = current_lat
            feedback.current_longitude = current_lon
            feedback.battery_remaining = max(0, battery)
            feedback.estimated_time_remaining = eta_seconds

            goal_handle.publish_feedback(feedback)

            if step % 8 == 0:  # Log every 8 steps
                self.get_logger().info(
                    f'  ✈️  Progress: {progress:.0f}% | '
                    f'Pos: ({current_lat:.4f}, {current_lon:.4f}) | '
                    f'ETA: {eta_seconds:.0f}s'
                )
            time.sleep(0.25)

        # ──────────────────────────────────────────────────────
        # PHASE 3: DELIVERING (50% → 70%)
        # ──────────────────────────────────────────────────────
        self._publish_state('DELIVERING')
        self.get_logger().info('📍 Phase 3: DELIVERING PACKAGE')

        for step in range(21):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return self._make_result(False, 'Cancelled during delivery', 0, 0)

            progress = 50.0 + step
            elapsed = time.time() - mission_start_time
            battery = initial_battery - (distance_km * battery_drain_per_km) - (elapsed * 0.05)
            hover_desc = ['Hovering...', 'Descending package...', 'Package release...'][min(step // 7, 2)]

            feedback.progress_percent = progress
            feedback.current_phase = 'DELIVERING_PACKAGE'
            feedback.status_message = f'📦 {hover_desc} Package: {goal.package_id}'
            feedback.current_latitude = goal.target_latitude
            feedback.current_longitude = goal.target_longitude
            feedback.battery_remaining = max(0, battery)
            feedback.estimated_time_remaining = float(distance_km * 1000 / self.drone_speed)

            goal_handle.publish_feedback(feedback)

            if step % 5 == 0:
                self.get_logger().info(
                    f'  📦 Delivering: {progress:.0f}% | {hover_desc}'
                )
            time.sleep(0.3)

        # Package delivered!
        self.get_logger().info(f'  ✅ Package {goal.package_id} delivered to {goal.destination_name}!')

        # ──────────────────────────────────────────────────────
        # PHASE 4: RETURN HOME (70% → 95%)
        # ──────────────────────────────────────────────────────
        self._publish_state('RETURNING')
        self.get_logger().info('📍 Phase 4: RETURNING TO HOME BASE')

        steps = 25
        for step in range(steps + 1):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return self._make_result(False, 'Cancelled during return', 0, 0)

            ratio = step / steps
            progress = 70.0 + (ratio * 25.0)
            elapsed = time.time() - mission_start_time
            battery = initial_battery - (distance_km * 2 * battery_drain_per_km * (0.5 + ratio * 0.5)) - elapsed * 0.05

            current_lat = goal.target_latitude + (self.home_latitude - goal.target_latitude) * ratio
            current_lon = goal.target_longitude + (self.home_longitude - goal.target_longitude) * ratio
            remaining_km = distance_km * (1 - ratio)
            eta_seconds = (remaining_km * 1000) / self.drone_speed

            feedback.progress_percent = progress
            feedback.current_phase = 'RETURNING_HOME'
            feedback.status_message = f'Returning to base — {remaining_km:.1f}km remaining'
            feedback.current_latitude = current_lat
            feedback.current_longitude = current_lon
            feedback.battery_remaining = max(0, battery)
            feedback.estimated_time_remaining = eta_seconds

            goal_handle.publish_feedback(feedback)

            if step % 8 == 0:
                self.get_logger().info(
                    f'  🔄 Return: {progress:.0f}% | ETA: {eta_seconds:.0f}s'
                )
            time.sleep(0.25)

        # ──────────────────────────────────────────────────────
        # PHASE 5: LANDING (95% → 100%)
        # ──────────────────────────────────────────────────────
        self._publish_state('LANDING')
        self.get_logger().info('📍 Phase 5: LANDING')

        for step in range(6):
            altitude = (5 - step) * 10
            progress = 95.0 + step
            elapsed = time.time() - mission_start_time
            battery = max(0, initial_battery - (distance_km * 2 * battery_drain_per_km) - elapsed * 0.05)

            feedback.progress_percent = progress
            feedback.current_phase = 'LANDING'
            feedback.status_message = f'Descending... {altitude}m above ground'
            feedback.current_latitude = self.home_latitude
            feedback.current_longitude = self.home_longitude
            feedback.battery_remaining = battery
            feedback.estimated_time_remaining = float(5 - step)

            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'  ↓ Altitude: {altitude}m')
            time.sleep(0.5)

        # ──────────────────────────────────────────────────────
        # MISSION COMPLETE!
        # ──────────────────────────────────────────────────────
        self._publish_state('IDLE')

        total_time = time.time() - mission_start_time
        total_distance = distance_km * 2  # Round trip

        goal_handle.succeed()  # Mark as succeeded

        # Build and return the final result
        result = DeliverPackage.Result()
        result.success = True
        result.message = (
            f'✅ MISSION COMPLETE! Package {goal.package_id} '
            f'delivered to {goal.destination_name}.'
        )
        result.delivery_time_seconds = total_time
        result.total_distance_km = total_distance

        self.get_logger().info('=' * 50)
        self.get_logger().info(f'  🏆 MISSION COMPLETE!')
        self.get_logger().info(f'  📦 Package: {goal.package_id}')
        self.get_logger().info(f'  📍 Delivered to: {goal.destination_name}')
        self.get_logger().info(f'  ⏱️  Mission time: {total_time:.1f}s')
        self.get_logger().info(f'  📏 Total distance: {total_distance:.2f} km')
        self.get_logger().info('=' * 50)

        return result

    def _publish_state(self, state):
        """Publish a state change command."""
        msg = String()
        msg.data = state
        self.state_pub.publish(msg)

    def _make_result(self, success, message, time_s, distance_km):
        """Helper to create a Result message."""
        result = DeliverPackage.Result()
        result.success = success
        result.message = message
        result.delivery_time_seconds = float(time_s)
        result.total_distance_km = float(distance_km)
        return result

    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate great-circle distance between two points using Haversine formula.
        Returns distance in kilometers.
        """
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) *
             math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c


def main(args=None):
    rclpy.init(args=args)
    node = DeliveryActionServer()

    # Use MultiThreadedExecutor to allow concurrent goal/cancel handling
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info('Delivery Action Server shutting down...')
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
PYEOF
```

## Delivery Action Client

**File:** `~/ros2_ws/src/drone_delivery_system/drone_delivery_system/delivery_action_client.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/drone_delivery_system/delivery_action_client.py << 'PYEOF'
#!/usr/bin/env python3
"""
Delivery Action Client
======================
Sends delivery missions and monitors mission progress live.

Usage:
  ros2 run drone_delivery_system delivery_action_client

Or via CLI:
  ros2 action send_goal /deliver_package \
    drone_delivery_interfaces/action/DeliverPackage \
    "{package_id: 'PKG-001', destination_name: 'SQU',
      target_latitude: 23.6097, target_longitude: 58.1804, max_speed: 15.0}" \
    --feedback
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from drone_delivery_interfaces.action import DeliverPackage


class DeliveryActionClient(Node):
    """Client for sending delivery missions to the action server."""

    def __init__(self):
        super().__init__('delivery_action_client')

        # Create the action client
        # (Same interface type and name must match the server!)
        self._action_client = ActionClient(
            self,
            DeliverPackage,      # Action type (same as server)
            '/deliver_package'   # Action name (same as server)
        )

        self.get_logger().info('Delivery Action Client ready')

    def send_mission(self, package_id, destination_name, latitude, longitude, speed=15.0):
        """
        Send a delivery mission goal to the action server.

        This is ASYNCHRONOUS — it doesn't block waiting for completion.
        The callbacks below handle the response when it arrives.
        """
        self.get_logger().info(
            f'⏳ Waiting for /deliver_package action server...'
        )

        # Wait for server to be available
        self._action_client.wait_for_server()

        # Build the goal
        goal = DeliverPackage.Goal()
        goal.package_id = package_id
        goal.destination_name = destination_name
        goal.target_latitude = latitude
        goal.target_longitude = longitude
        goal.max_speed = speed

        self.get_logger().info('=' * 55)
        self.get_logger().info(f'  🚀 SENDING DELIVERY MISSION')
        self.get_logger().info(f'  Package : {package_id}')
        self.get_logger().info(f'  To      : {destination_name}')
        self.get_logger().info(f'  Coords  : ({latitude:.4f}°N, {longitude:.4f}°E)')
        self.get_logger().info(f'  Speed   : {speed} m/s')
        self.get_logger().info('=' * 55)

        # Send the goal ASYNCHRONOUSLY
        # feedback_callback is called every time server publishes feedback
        send_goal_future = self._action_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )

        # Add callback for when goal is accepted/rejected
        send_goal_future.add_done_callback(self.goal_response_callback)

    # ============================================================
    # CALLBACK 1: Goal was accepted or rejected
    # ============================================================
    def goal_response_callback(self, future):
        """Called when the server responds to our goal submission."""
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('❌ Mission REJECTED by server!')
            return

        self.get_logger().info('✅ Mission ACCEPTED! Delivery in progress...')
        self.get_logger().info('─' * 55)

        # Set up callback for when the mission finishes
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    # ============================================================
    # CALLBACK 2: Feedback from the server during mission
    # ============================================================
    def feedback_callback(self, feedback_msg):
        """Called continuously as the server publishes progress updates."""
        fb = feedback_msg.feedback

        # Build a progress bar
        bar_length = 25
        filled = int(fb.progress_percent / 100 * bar_length)
        bar = f'[{"█" * filled}{"░" * (bar_length - filled)}]'

        # Phase emoji
        phase_emoji = {
            'TAKEOFF': '🚀',
            'FLYING_TO_DESTINATION': '✈️ ',
            'DELIVERING_PACKAGE': '📦',
            'RETURNING_HOME': '🔄',
            'LANDING': '🛬',
        }.get(fb.current_phase, '❓')

        self.get_logger().info(
            f'{phase_emoji} {bar} {fb.progress_percent:5.1f}% | '
            f'🔋{fb.battery_remaining:.0f}% | '
            f'⏱️ {fb.estimated_time_remaining:.0f}s | '
            f'{fb.status_message}'
        )

    # ============================================================
    # CALLBACK 3: Final result
    # ============================================================
    def result_callback(self, future):
        """Called when the mission is complete (success, failure, or cancel)."""
        result_response = future.result()
        result = result_response.result
        status = result_response.status

        self.get_logger().info('─' * 55)

        if result.success:
            self.get_logger().info('🏆 DELIVERY COMPLETE!')
            self.get_logger().info(f'  {result.message}')
            self.get_logger().info(f'  Distance: {result.total_distance_km:.2f} km')
            self.get_logger().info(f'  Time    : {result.delivery_time_seconds:.1f} seconds')
        else:
            self.get_logger().error(f'❌ DELIVERY FAILED: {result.message}')

        # Shutdown after mission
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    client = DeliveryActionClient()

    # Send the delivery mission
    client.send_mission(
        package_id='PKG-2024-001',
        destination_name='Sultan Qaboos University',
        latitude=23.6097,
        longitude=58.1804,
        speed=15.0
    )

    # Keep running to receive callbacks
    rclpy.spin(client)


if __name__ == '__main__':
    main()
PYEOF
```

## Build and Test Actions

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

**Terminal 1:** Start the action server:
```bash
ros2 run drone_delivery_system delivery_action_server
```

**Terminal 2:** Send a delivery mission:
```bash
ros2 run drone_delivery_system delivery_action_client
```

**Expected Output (Terminal 2):**
```
[INFO] [delivery_action_client]: =====================================================
[INFO] [delivery_action_client]:   🚀 SENDING DELIVERY MISSION
[INFO] [delivery_action_client]:   Package : PKG-2024-001
[INFO] [delivery_action_client]:   To      : Sultan Qaboos University
[INFO] [delivery_action_client]: ✅ Mission ACCEPTED! Delivery in progress...
[INFO] [delivery_action_client]: 🚀 [░░░░░░░░░░░░░░░░░░░░░░░░░]  0.0% | 🔋100% | ⏱️ 3600s | Ascending...
[INFO] [delivery_action_client]: 🚀 [██░░░░░░░░░░░░░░░░░░░░░░░]  5.0% | 🔋99%  | ⏱️ 3400s | Ascending... 25m
[INFO] [delivery_action_client]: ✈️  [████░░░░░░░░░░░░░░░░░░░░░] 10.0% | 🔋98%  | En route to SQU
...
[INFO] [delivery_action_client]: 🏆 DELIVERY COMPLETE!
[INFO] [delivery_action_client]:   Distance: 52.8 km
[INFO] [delivery_action_client]:   Time    : 31.2 seconds
```

**Test via CLI (no client code needed):**
```bash
# List all actions
ros2 action list

# Show action interface
ros2 action info /deliver_package

# Send goal from command line (--feedback shows live updates)
ros2 action send_goal /deliver_package \
  drone_delivery_interfaces/action/DeliverPackage \
  "{package_id: 'PKG-CLI-001', destination_name: 'Muttrah Corniche',
    target_latitude: 23.6177, target_longitude: 58.5902, max_speed: 15.0}" \
  --feedback
```

---

# PART 8 — PARAMETERS

## What Are Parameters?

Parameters are **named values stored inside a node** that can be read and changed at runtime. They replace hardcoded values with configurable ones.

```python
# Without parameters (BAD):
DRONE_SPEED = 15.0  # Hardcoded — must recompile to change

# With parameters (GOOD):
self.declare_parameter('drone_speed', 15.0)  # Configurable at runtime!
speed = self.get_parameter('drone_speed').get_parameter_value().double_value
```

**Why parameters matter for drones:**
- Different delivery routes need different speeds
- Weather conditions change safe altitude limits
- Battery thresholds vary by battery model
- No recompile or restart needed — change live!

## Working with Parameters

### Declare Parameters (in your node's `__init__`):
```python
# Declare with default values
self.declare_parameter('drone_speed_ms', 15.0)
self.declare_parameter('max_altitude', 120.0)
self.declare_parameter('battery_warning_threshold', 20.0)
self.declare_parameter('home_location', 'Muscat')
self.declare_parameter('auto_return_on_low_battery', True)
```

### Read Parameters:
```python
# Different types need different getters
speed = self.get_parameter('drone_speed_ms').get_parameter_value().double_value
altitude = self.get_parameter('max_altitude').get_parameter_value().double_value
threshold = self.get_parameter('battery_warning_threshold').get_parameter_value().double_value
location = self.get_parameter('home_location').get_parameter_value().string_value
auto_return = self.get_parameter('auto_return_on_low_battery').get_parameter_value().bool_value
```

### Live Parameter Updates (Parameter Callback):
```python
from rcl_interfaces.msg import ParameterEvent, SetParametersResult

def __init__(self):
    # ... other setup ...
    
    # Register callback for parameter changes
    self.add_on_set_parameters_callback(self.parameters_callback)

def parameters_callback(self, params):
    """Called automatically when ANY parameter is changed via ros2 param set."""
    for param in params:
        if param.name == 'drone_speed_ms':
            old_speed = self.drone_speed
            self.drone_speed = param.value
            self.get_logger().info(
                f'Speed updated: {old_speed} → {self.drone_speed} m/s'
            )
        elif param.name == 'battery_warning_threshold':
            self.warning_threshold = param.value
            self.get_logger().info(
                f'Battery warning: {self.warning_threshold}%'
            )
    
    # Return success — you could validate and return failure here
    return SetParametersResult(successful=True)
```

## Parameter CLI Commands

```bash
# List ALL parameters for ALL nodes
ros2 param list

# List parameters for a specific node
ros2 param list /battery_monitor_node
```
Output:
```
/battery_monitor_node:
  battery_warning_threshold
  discharge_rate
  initial_battery
  use_sim_time
```

```bash
# Get a specific parameter value
ros2 param get /battery_monitor_node battery_warning_threshold
```
Output:
```
Double value is: 20.0
```

```bash
# SET a parameter LIVE (no restart needed!)
ros2 param set /battery_monitor_node battery_warning_threshold 30.0
```
Output:
```
Set parameter successful
```

```bash
# The node will immediately warn at 30% instead of 20%!
ros2 param set /delivery_action_server drone_speed_ms 25.0
# Drone now flies faster — applies to NEXT mission

# Dump all parameters to a YAML file
ros2 param dump /battery_monitor_node --output-dir /tmp/

# Load parameters from YAML at startup
ros2 run drone_delivery_system battery_monitor_node \
  --ros-args --params-file /tmp/battery_monitor_node.yaml
```

## Setting Parameters at Launch (in setup.py or launch file):

```bash
# Set parameters via command line at startup
ros2 run drone_delivery_system battery_monitor_node \
  --ros-args \
  -p battery_warning_threshold:=25.0 \
  -p discharge_rate:=1.0 \
  -p initial_battery:=85.0
```

---

# PART 9 — LAUNCH FILES

## Why Launch Files?

Running 7+ separate terminals for 7 nodes is tedious, error-prone, and doesn't scale. Launch files solve this.

```
Without launch file:              With launch file:
Terminal 1: drone_status_node     $ ros2 launch drone_delivery_system \
Terminal 2: battery_monitor_node       drone_delivery.launch.py
Terminal 3: gps_node              → All nodes start automatically!
Terminal 4: ground_control_node
Terminal 5: takeoff_service_server
Terminal 6: destination_service_server
Terminal 7: delivery_action_server
```

## The Launch File

**File:** `~/ros2_ws/src/drone_delivery_system/launch/drone_delivery.launch.py`

```bash
cat > ~/ros2_ws/src/drone_delivery_system/launch/drone_delivery.launch.py << 'PYEOF'
#!/usr/bin/env python3
"""
Drone Delivery System — Complete Launch File
=============================================
Starts ALL nodes for the drone delivery system in one command:
  ros2 launch drone_delivery_system drone_delivery.launch.py

Optional arguments:
  drone_speed:=20.0           Override drone speed
  max_altitude:=150.0         Override max altitude
  battery_warning:=25.0       Override battery warning threshold
  debug:=true                 Enable verbose logging

Example:
  ros2 launch drone_delivery_system drone_delivery.launch.py \
    drone_speed:=20.0 battery_warning:=25.0
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import (
    DeclareLaunchArgument,
    LogInfo,
    TimerAction
)
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    """
    This function MUST be named generate_launch_description().
    ROS2 calls this function when the launch file is executed.
    It returns a LaunchDescription object containing everything to run.
    """

    # ============================================================
    # STEP 1: DECLARE LAUNCH ARGUMENTS
    # These allow overriding values from command line:
    #   ros2 launch ... drone_speed:=25.0
    # ============================================================
    drone_speed_arg = DeclareLaunchArgument(
        'drone_speed',
        default_value='15.0',
        description='Drone cruising speed in meters per second'
    )

    max_altitude_arg = DeclareLaunchArgument(
        'max_altitude',
        default_value='120.0',
        description='Maximum flight altitude in meters (regulations apply!)'
    )

    battery_warning_arg = DeclareLaunchArgument(
        'battery_warning',
        default_value='20.0',
        description='Battery level % to trigger low battery warning'
    )

    home_lat_arg = DeclareLaunchArgument(
        'home_latitude',
        default_value='23.5880',
        description='Home base latitude (Muscat, Oman default)'
    )

    home_lon_arg = DeclareLaunchArgument(
        'home_longitude',
        default_value='58.3829',
        description='Home base longitude (Muscat, Oman default)'
    )

    # Access argument values using LaunchConfiguration
    drone_speed = LaunchConfiguration('drone_speed')
    max_altitude = LaunchConfiguration('max_altitude')
    battery_warning = LaunchConfiguration('battery_warning')
    home_lat = LaunchConfiguration('home_latitude')
    home_lon = LaunchConfiguration('home_longitude')

    # ============================================================
    # STEP 2: DEFINE NODES
    # ============================================================

    # Node 1: Drone Status
    drone_status_node = Node(
        package='drone_delivery_system',      # Package name (from setup.py)
        executable='drone_status_node',        # Entry point name (from setup.py)
        name='drone_status_node',              # Node name (overrides the one in code)
        output='screen',                       # Show output in terminal
        emulate_tty=True,                      # Enable colored output
    )

    # Node 2: Battery Monitor (with parameters)
    battery_monitor_node = Node(
        package='drone_delivery_system',
        executable='battery_monitor_node',
        name='battery_monitor_node',
        output='screen',
        emulate_tty=True,
        parameters=[{                          # Pass parameters to the node
            'battery_warning_threshold': battery_warning,
            'initial_battery': 100.0,
            'discharge_rate': 0.3,
        }]
    )

    # Node 3: GPS
    gps_node = Node(
        package='drone_delivery_system',
        executable='gps_node',
        name='gps_node',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'home_latitude': home_lat,
            'home_longitude': home_lon,
            'home_altitude': 50.0,
        }]
    )

    # Node 4: Ground Control (delayed start — wait for telemetry nodes)
    ground_control_node = Node(
        package='drone_delivery_system',
        executable='ground_control_node',
        name='ground_control_node',
        output='screen',
        emulate_tty=True,
    )

    # Node 5: Takeoff/Land Service
    takeoff_service_server = Node(
        package='drone_delivery_system',
        executable='takeoff_service_server',
        name='takeoff_service_server',
        output='screen',
        emulate_tty=True,
    )

    # Node 6: Destination Service
    destination_service_server = Node(
        package='drone_delivery_system',
        executable='destination_service_server',
        name='destination_service_server',
        output='screen',
        emulate_tty=True,
    )

    # Node 7: Delivery Action Server (with parameters)
    delivery_action_server = Node(
        package='drone_delivery_system',
        executable='delivery_action_server',
        name='delivery_action_server',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'drone_speed_ms': drone_speed,
            'max_altitude': max_altitude,
            'delivery_hover_time': 10.0,
        }]
    )

    # ============================================================
    # STEP 3: ASSEMBLE THE LAUNCH DESCRIPTION
    # Order matters for LogInfo messages; nodes start roughly in order
    # but ROS2 doesn't guarantee sequential startup
    # ============================================================
    return LaunchDescription([
        # Print startup message
        LogInfo(msg=''),
        LogInfo(msg='🚁 ═══════════════════════════════════════════════'),
        LogInfo(msg='🚁    DRONE DELIVERY SYSTEM — STARTING UP        '),
        LogInfo(msg='🚁 ═══════════════════════════════════════════════'),

        # Declare arguments first (order matters)
        drone_speed_arg,
        max_altitude_arg,
        battery_warning_arg,
        home_lat_arg,
        home_lon_arg,

        # Core telemetry nodes
        drone_status_node,
        battery_monitor_node,
        gps_node,

        # Ground control (slight delay so telemetry is ready)
        TimerAction(period=1.0, actions=[ground_control_node]),

        # Service and action servers
        takeoff_service_server,
        destination_service_server,
        delivery_action_server,

        LogInfo(msg='✅ All nodes launched! System ready.'),
        LogInfo(msg=''),
        LogInfo(msg='Available commands:'),
        LogInfo(msg='  ros2 service call /takeoff std_srvs/srv/Trigger {}'),
        LogInfo(msg='  ros2 service call /land std_srvs/srv/Trigger {}'),
        LogInfo(msg='  ros2 action send_goal /deliver_package ...'),
        LogInfo(msg=''),
    ])
PYEOF
```

## Build and Launch

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash

# Launch with defaults
ros2 launch drone_delivery_system drone_delivery.launch.py

# Launch with custom parameters
ros2 launch drone_delivery_system drone_delivery.launch.py \
  drone_speed:=20.0 \
  battery_warning:=25.0 \
  max_altitude:=100.0
```

**Expected Output:**
```
[INFO] [launch]: 🚁 ═══════════════════════════════════════════════
[INFO] [launch]: 🚁    DRONE DELIVERY SYSTEM — STARTING UP
[INFO] [launch]: ✅ All nodes launched! System ready.

[drone_status_node]: 📡 Status: [IDLE]
[battery_monitor_node]: 🟢 Battery: 99.4% [█████████░]
[gps_node]: 📍 GPS: 23.588005°N, 58.382900°E, Alt: 50.0m
[ground_control_node]: 🛰️  Ground Control Station — ONLINE
```

---

# PART 10 — VISUALIZATION & DEBUGGING

## Tool 1: rqt_graph — See Node Communication

```bash
# Launch in background (while system is running)
rqt_graph &
```

This opens a GUI showing:
```
        [/battery_status]
gps_node ──/gps_location──→ ground_control_node
drone_status_node ──/drone_status──→ ground_control_node
battery_monitor_node ──/battery_status──→ ground_control_node
```

## Tool 2: ros2 doctor — Health Check

```bash
ros2 doctor
```
Output:
```
   All    1 ROS 2 packages
   All checks passed

   Found 7 nodes:
   /battery_monitor_node
   /delivery_action_server
   /destination_service_server
   /drone_status_node
   /gps_node
   /ground_control_node
   /takeoff_service_server
```

## Tool 3: Topic Debugging

```bash
# Live data monitoring
ros2 topic echo /battery_status
ros2 topic echo /gps_location
ros2 topic echo /drone_status

# Check publish rate
ros2 topic hz /battery_status   # Should be ~0.5 Hz
ros2 topic hz /gps_location     # Should be ~1.0 Hz

# Check publishers and subscribers
ros2 topic info /gps_location --verbose

# Check message bandwidth
ros2 topic bw /gps_location
```

## Tool 4: Node Inspection

```bash
# Full info about a node
ros2 node info /delivery_action_server
```
Output:
```
/delivery_action_server
  Subscribers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
  Publishers:
    /drone_state_command: std_msgs/msg/String
    /rosout: rcl_interfaces/msg/Log
  Service Servers:
    /delivery_action_server/describe_parameters
    /delivery_action_server/get_parameter_types
    ...
  Action Servers:
    /deliver_package: drone_delivery_interfaces/action/DeliverPackage
```

## Tool 5: Logging Levels

Control what gets printed:
```bash
# Set log level for a node (DEBUG shows everything)
ros2 run drone_delivery_system battery_monitor_node \
  --ros-args --log-level DEBUG

# Set log level for specific logger
ros2 run drone_delivery_system battery_monitor_node \
  --ros-args --log-level battery_monitor_node:=WARN
```

Log levels (most → least verbose):
```
DEBUG → INFO → WARN → ERROR → FATAL
```

## Common Beginner Mistakes & Fixes

### ❌ Mistake 1: Forgetting to source
```bash
# SYMPTOM:
$ ros2 run drone_delivery_system drone_status_node
# Error: No executable found

# FIX:
source ~/ros2_ws/install/setup.bash
# Or add to ~/.bashrc (one-time fix)
```

### ❌ Mistake 2: Building without sourcing afterwards
```bash
# SYMPTOM: Code changes not reflected after build

# FIX:
colcon build
source install/setup.bash  # ← MUST do this after EVERY build!
```

### ❌ Mistake 3: Wrong package name in setup.py
```python
# SYMPTOM: ros2 run finds no executable
# FIX: Check setup.py entry_points — name must match exactly
'drone_status_node = drone_delivery_system.drone_status_node:main',
#    ↑ executable name           ↑ module                 ↑ function
```

### ❌ Mistake 4: Interfaces not built first
```bash
# SYMPTOM: ImportError: cannot import name 'ChangeDestination'

# FIX: Build interfaces package BEFORE main package
colcon build --packages-select drone_delivery_interfaces
source install/setup.bash
colcon build --packages-select drone_delivery_system
source install/setup.bash
```

### ❌ Mistake 5: Missing `return response` in service callback
```python
# SYMPTOM: Service client hangs forever

# FIX: Always return the response in service callbacks
def my_service_callback(self, request, response):
    response.success = True
    return response  # ← NEVER forget this!
```

### ❌ Mistake 6: Not using MultiThreadedExecutor with ActionServer
```bash
# SYMPTOM: Cancel requests are ignored during execution

# FIX: Use MultiThreadedExecutor in action server main()
executor = MultiThreadedExecutor()
executor.add_node(node)
executor.spin()
```

### ❌ Mistake 7: Topic name mismatch
```python
# SYMPTOM: Subscriber receives nothing despite publisher running

# Publisher publishes to:
self.create_publisher(Float32, '/battery_status', 10)  # Note the /

# Subscriber must match EXACTLY:
self.create_subscription(Float32, '/battery_status', callback, 10)  # Same /
```

## Debugging Workflow Checklist

When something doesn't work:

```
1. Is the workspace sourced?
   → source ~/ros2_ws/install/setup.bash

2. Did you build after the last code change?
   → colcon build && source install/setup.bash

3. Is the node running?
   → ros2 node list

4. Is the topic being published?
   → ros2 topic list
   → ros2 topic echo /your_topic

5. Do topic names match between publisher and subscriber?
   → ros2 topic info /your_topic --verbose

6. Is the service available?
   → ros2 service list
   → ros2 service type /your_service

7. Are interfaces built?
   → ros2 interface show package/srv/YourService

8. Check the logs for errors
   → Look at terminal output where node runs
   → ros2 run ... --ros-args --log-level DEBUG
```

---

# PART 11 — FINAL INTEGRATED DEMO

## Complete System Demo Sequence

Run each command in a new terminal tab after launching the system.

### Step 1: Launch the Complete System

```bash
# Terminal 1 (main)
source ~/ros2_ws/install/setup.bash
ros2 launch drone_delivery_system drone_delivery.launch.py
```

You'll see all 7 nodes starting and telemetry flowing.

### Step 2: Verify System is Healthy (Terminal 2)

```bash
source ~/ros2_ws/install/setup.bash

# Check all nodes are running
ros2 node list
# Expected: 7 nodes

# Check topics are publishing
ros2 topic list
# Expected: /battery_status, /gps_location, /drone_status + more

# Quick system health check
ros2 doctor --report
```

### Step 3: View Live Telemetry (Terminal 2)

```bash
# Watch battery in real-time
ros2 topic echo /battery_status --once

# Watch GPS
ros2 topic echo /gps_location --once

# Monitor status
ros2 topic echo /drone_status
```

### Step 4: Send Takeoff Command (Terminal 2)

```bash
ros2 service call /takeoff std_srvs/srv/Trigger {}
```

**Output:**
```
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(
  success=True,
  message='✅ TAKEOFF CONFIRMED: Drone ascending to 50.0m...'
)
```

Watch Terminal 1 — you'll see drone_status change to `TAKING_OFF`!

### Step 5: Change Delivery Destination (Terminal 2)

```bash
ros2 service call /change_destination \
  drone_delivery_interfaces/srv/ChangeDestination \
  "{latitude: 23.6097, longitude: 58.1804, destination_name: 'Sultan Qaboos University'}"
```

**Output:**
```
response:
  success: True
  message: ✅ Destination updated! Home Base → Sultan Qaboos University
  previous_destination: Home Base
```

### Step 6: Launch Delivery Mission (Terminal 2)

```bash
ros2 action send_goal /deliver_package \
  drone_delivery_interfaces/action/DeliverPackage \
  "{package_id: 'PKG-2024-001',
    destination_name: 'Sultan Qaboos University',
    target_latitude: 23.6097,
    target_longitude: 58.1804,
    max_speed: 15.0}" \
  --feedback
```

**Live Output:**
```
Goal accepted with ID: a3b7c9...

Feedback:
    progress_percent: 0.0
    current_phase: TAKEOFF
    status_message: Ascending... 0m / 50m
    battery_remaining: 99.9

Feedback:
    progress_percent: 5.0
    current_phase: TAKEOFF
    ...

Feedback:
    progress_percent: 10.0
    current_phase: FLYING_TO_DESTINATION
    status_message: En route to Sultan Qaboos University — 24.8km remaining

...

Feedback:
    progress_percent: 50.0
    current_phase: DELIVERING_PACKAGE
    status_message: 📦 Hovering... Package: PKG-2024-001

...

Feedback:
    progress_percent: 95.0
    current_phase: LANDING
    status_message: Descending... 50m above ground

Result:
    success: True
    message: ✅ MISSION COMPLETE! Package PKG-2024-001 delivered to SQU.
    delivery_time_seconds: 28.5
    total_distance_km: 49.6
```

### Step 7: Dynamic Parameter Update During Mission (Terminal 3)

While a mission is running, you can update parameters live:

```bash
# Speed up the drone mid-mission!
ros2 param set /delivery_action_server drone_speed_ms 25.0

# Lower battery warning threshold
ros2 param set /battery_monitor_node battery_warning_threshold 30.0

# Verify the change
ros2 param get /battery_monitor_node battery_warning_threshold
```

### Step 8: View the Communication Graph

```bash
# Open rqt_graph to see ALL node connections
rqt_graph
```

You'll see the complete system graph:
```
gps_node ────────────────────────────────→ ground_control_node
battery_monitor_node ───────────────────→ ground_control_node
drone_status_node ──────────────────────→ ground_control_node
delivery_action_server ─────────────────→ drone_status_node (via /drone_state_command)
```

### Complete Terminal Output from Terminal 1 (Launch)

```
[drone_status_node]:     📡 Status: [IDLE]
[battery_monitor_node]:  🟢 Battery: 99.4% [█████████░]
[gps_node]:              📍 GPS: 23.588005°N, 58.382900°E, Alt: 50.0m
[ground_control_node]:   ════════════════════════════════
[ground_control_node]:      GROUND CONTROL DASHBOARD
[ground_control_node]:   ════════════════════════════════
[ground_control_node]:     ⏸️  Status    : IDLE
[ground_control_node]:     🔋 Battery   : 99.4% [█████████░] ✅ OK
[ground_control_node]:     📍 GPS Lat   : 23.588005°
[ground_control_node]:     📍 GPS Lon   : 58.382900°
[ground_control_node]:     🏔️  Altitude  : 50.0 m
[ground_control_node]:   ════════════════════════════════

[takeoff_service_server]: 🚀 TAKEOFF! Ascending to 50.0m
[drone_status_node]:      State transition: IDLE → TAKING_OFF
[drone_status_node]:      📡 Status: [TAKING_OFF]

[destination_service_server]: 📍 Destination: Home Base → Sultan Qaboos University

[delivery_action_server]: Mission started: PKG-2024-001 → Sultan Qaboos University
[delivery_action_server]: Phase 1: TAKEOFF
[delivery_action_server]:   ↑ Altitude: 0m | Battery: 100.0%
[delivery_action_server]:   ↑ Altitude: 5m | Battery: 99.9%
...
[delivery_action_server]: Phase 2: FLYING TO Sultan Qaboos University (24.8 km)
[delivery_action_server]:   ✈️  Progress: 10% | Pos: (23.5904, 58.3730) | ETA: 1653s
...
[delivery_action_server]: 🏆 MISSION COMPLETE!
[delivery_action_server]:   Package: PKG-2024-001
[delivery_action_server]:   Delivered to: Sultan Qaboos University
[drone_status_node]:      State transition: LANDING → IDLE
```

---

# PART 12 — WORKSHOP MATERIALS

## 12.1 — Workshop Timeline (2.5 Hours)

| Time | Duration | Activity |
|------|----------|---------|
| 0:00 | 10 min | Welcome, goals, system check |
| 0:10 | 15 min | **Part 1:** ROS2 concepts, architecture diagram |
| 0:25 | 10 min | **Part 2:** Create workspace, colcon build |
| 0:35 | 15 min | **Part 3:** Create packages, interfaces |
| 0:50 | 20 min | **Part 4:** Create 3 nodes, ros2 node list |
| 1:10 | 10 min | ☕ BREAK + Q&A |
| 1:20 | 20 min | **Part 5:** Topics, ground control dashboard |
| 1:40 | 20 min | **Part 6:** Services, takeoff/land |
| 2:00 | 20 min | **Part 7:** Actions, full delivery mission |
| 2:20 | 10 min | **Part 8-9:** Parameters, launch file |
| 2:30 | 10 min | **Part 10-11:** Debug tools, final demo |
| 2:40 | 20 min | Student exercises (choose one) |
| 3:00 | — | Q&A, Part 13 preview, wrap up |

---

## 12.2 — Instructor Teaching Script

### Opening (10 min)
> "Today you're going to build software that could power a real delivery drone. Not a toy demo — a real architecture used by companies like Amazon and DHL. By the end of today, you'll be able to read and write ROS2 code, which is a skill that gets you into aerospace, autonomous vehicles, medical robotics, and more."

### Part 1 Teaching Tips
- Draw the node-topic-service diagram on whiteboard FIRST
- Ask: "Why would a GPS module and flight controller be separate programs?"
- Real answer: If GPS crashes, flight controller keeps running
- Use the DHL/Amazon comparison to make it tangible

### Part 4 Teaching Tips (Nodes)
> "Think of each node like a specialist on a team. The GPS specialist only does GPS. The battery specialist only does battery. They communicate through a shared message board [topic]. Nobody talks directly — it's all through the board."

### Part 5 Teaching Tips (Topics)
- Draw publisher → topic → subscriber on whiteboard
- Run `ros2 topic echo /battery_status` and show live data
- Ask students to predict what Hz will show before running
- Key phrase: "Topics are asynchronous — sender doesn't care if anyone is listening"

### Part 6 Teaching Tips (Services)
- Compare to a phone call vs. a radio broadcast
- Topics = radio (no guarantee anyone hears)
- Services = phone call (one-to-one, guaranteed response)

### Part 7 Teaching Tips (Actions)
- Compare to ordering food delivery:
  - Goal = "I want pizza delivered to my address" 
  - Feedback = "Your order is 2km away"
  - Result = "Delivered! Here's your receipt"
- "Why not just use a service?" → Services time out, no progress updates

---

## 12.3 — Live Demo Sequence

Run this sequence in front of students to show the complete system:

```bash
# Window 1: Launch everything
ros2 launch drone_delivery_system drone_delivery.launch.py

# Window 2: Show system is alive
ros2 node list
ros2 topic list
ros2 topic echo /battery_status

# Window 3: Show graph (visual)
rqt_graph

# Window 4: Interactive commands
ros2 service call /takeoff std_srvs/srv/Trigger {}
ros2 param set /battery_monitor_node discharge_rate 5.0  # Fast drain!
ros2 action send_goal /deliver_package ... --feedback
```

---

## 12.4 — Student Exercises

### 🟢 Exercise 1 — Easy (15 min): New Telemetry Topic
Add a `/wind_speed` topic to the system.

Tasks:
1. Create a new file `wind_sensor_node.py`
2. Publish `Float32` to `/wind_speed` every 2 seconds
3. Simulate wind 0–20 m/s (use `random.uniform(0, 20)`)
4. Subscribe to it in `ground_control_node.py`
5. Display it in the dashboard

Starter code:
```python
import random
from std_msgs.msg import Float32

class WindSensorNode(Node):
    def __init__(self):
        super().__init__('wind_sensor_node')
        self.pub = self.create_publisher(Float32, '/wind_speed', 10)
        self.timer = self.create_timer(2.0, self.publish_wind)
    
    def publish_wind(self):
        msg = Float32()
        msg.data = random.uniform(0.0, 20.0)
        self.pub.publish(msg)
        self.get_logger().info(f'💨 Wind: {msg.data:.1f} m/s')
```

---

### 🟡 Exercise 2 — Medium (20 min): Drone Info Service
Create a new service `/get_drone_info` that returns drone information.

Tasks:
1. Add `DroneInfo.srv` to the interfaces package:
   ```
   ---
   string drone_model
   string serial_number
   string firmware_version
   float32 max_payload_kg
   float32 max_range_km
   ```
2. Create `drone_info_service.py` with a server
3. Rebuild interfaces and main package
4. Test with `ros2 service call /get_drone_info ...`

---

### 🟡 Exercise 3 — Medium (20 min): Dynamic Parameter Monitor
Add automatic behavior when battery gets low.

Tasks:
1. In `battery_monitor_node.py`, add a parameter `auto_rtb_enabled` (bool, default: True)
2. When battery drops below `battery_warning_threshold`:
   - If `auto_rtb_enabled` is True, publish `'RETURNING'` to `/drone_state_command`
   - Log a warning with countdown
3. Test by lowering `discharge_rate` to 10.0:
   ```bash
   ros2 param set /battery_monitor_node discharge_rate 10.0
   ```

---

### 🔴 Exercise 4 — Hard (30 min): Mission Planner Node
Create a `mission_planner_node.py` that:
1. Subscribes to `/battery_status`
2. Automatically refuses to start missions when battery < 40%
3. Has a `/queue_delivery` service that accepts deliveries and queues them
4. Automatically sends the next queued delivery via the action client when ready
5. Has a parameter `min_battery_for_mission` (default: 40.0)

---

## 12.5 — Quiz Questions

### Multiple Choice

**Q1.** What is the difference between a ROS2 Topic and a Service?
- A) Topics are faster than services
- B) Topics are publish/subscribe (one-to-many), services are request/response (one-to-one) ✓
- C) Services can only be used for drone commands
- D) Topics require a master node

**Q2.** When should you use an Action instead of a Service?
- A) When you need a response immediately
- B) When multiple nodes need to subscribe
- C) When the task takes a long time and you need progress updates ✓
- D) When you need to broadcast data continuously

**Q3.** What command shows all currently running ROS2 nodes?
- A) `ros2 topic list`
- B) `ros2 node list` ✓
- C) `ros2 run --list`
- D) `ros2 pkg list`

**Q4.** What does `rclpy.spin(node)` do?
- A) Rotates the drone
- B) Starts the node and runs it once
- C) Keeps the node running and processes all incoming callbacks ✓
- D) Sends a heartbeat message

**Q5.** In this code, what is 10 in `create_publisher(Float32, '/battery', 10)`?
- A) The publish rate in Hz
- B) The timeout in seconds
- C) The QoS queue size (how many messages to buffer) ✓
- D) The message priority

**Q6.** Why do we call `colcon build` AND `source install/setup.bash`?
- A) `colcon build` is optional; source is the important one
- B) `colcon build` compiles the code; source makes it available to the shell ✓
- C) They are interchangeable
- D) `source` compiles and `colcon build` installs

**Q7.** What happens if a Service callback doesn't return `response`?
- A) Nothing — it's optional
- B) The service fails silently
- C) The client hangs forever waiting for a response ✓
- D) ROS2 returns a default response

**Q8.** Which folder in your workspace should you NEVER delete?
- A) `build/`
- B) `install/`
- C) `log/`
- D) `src/` ✓

### Short Answer

**Q9.** Name 3 real-world use cases where you would use a ROS2 Action instead of a Service.
> Sample answer: Autonomous navigation (go to waypoint), SLAM mapping (scan an area), manipulation task (pick and place object), delivery mission, charging docking.

**Q10.** What is the purpose of the `drone_delivery_interfaces` package? Why is it separate from `drone_delivery_system`?
> Sample answer: It contains custom message definitions (.srv and .action files). It's separate because interface definitions use CMake (ament_cmake) while our nodes use Python (ament_python). Separating them allows other packages to import our interfaces without depending on our entire node implementation.

**Q11.** Describe in one sentence what `ros2 param set /battery_monitor_node discharge_rate 2.0` does.
> Sample answer: Changes the battery discharge rate of the running battery_monitor_node from its current value to 2.0% per second without restarting the node.

---

## 12.6 — ROS2 Command Cheat Sheet

```
══════════════════════════════════════════════════════
            ROS2 COMMAND QUICK REFERENCE
══════════════════════════════════════════════════════

WORKSPACE
─────────────────────────────────────────────────────
colcon build                    Build all packages
colcon build --packages-select PKG   Build one package
colcon build --symlink-install  Build with live Python edit
source install/setup.bash       Activate workspace

NODES
─────────────────────────────────────────────────────
ros2 node list                  List running nodes
ros2 node info /node_name       Show node details
ros2 run PKG EXECUTABLE         Run a node
ros2 run PKG EXEC --ros-args -p KEY:=VAL  Run with params

TOPICS
─────────────────────────────────────────────────────
ros2 topic list                 List all topics
ros2 topic echo /topic          Print topic messages
ros2 topic echo /topic --once   Print one message
ros2 topic hz /topic            Show publish rate
ros2 topic info /topic          Show type, pub/sub count
ros2 topic bw /topic            Show bandwidth
ros2 topic pub /topic TYPE DATA Publish manually

SERVICES
─────────────────────────────────────────────────────
ros2 service list               List all services
ros2 service type /service      Show service type
ros2 service call /srv TYPE {}  Call a service
ros2 interface show TYPE        Show message fields

ACTIONS
─────────────────────────────────────────────────────
ros2 action list                List all actions
ros2 action info /action        Show action details
ros2 action send_goal /action TYPE GOAL     Send goal
ros2 action send_goal ... --feedback        With feedback

PARAMETERS
─────────────────────────────────────────────────────
ros2 param list                 List all parameters
ros2 param list /node           List node's parameters
ros2 param get /node KEY        Get parameter value
ros2 param set /node KEY VALUE  Set parameter live
ros2 param dump /node           Print all params as YAML

LAUNCH
─────────────────────────────────────────────────────
ros2 launch PKG FILE.launch.py  Launch a launch file
ros2 launch PKG FILE.launch.py KEY:=VAL  With args

PACKAGES
─────────────────────────────────────────────────────
ros2 pkg list                   List all packages
ros2 pkg create NAME --build-type TYPE --dependencies DEPS
ros2 interface list             List all message types
ros2 interface show TYPE        Show type fields

DEBUGGING
─────────────────────────────────────────────────────
ros2 doctor                     Health check
ros2 doctor --report            Detailed report
rqt_graph                       Visual node graph
rqt_console                     Log viewer GUI
ros2 bag record -a              Record all topics
ros2 bag play FILE.bag          Replay recording

══════════════════════════════════════════════════════
```

---

## 12.7 — Troubleshooting Guide

### Problem: `No executable found`
```bash
# Cause: setup.py entry_points not matching, or not built
# Fix:
colcon build --packages-select drone_delivery_system
source install/setup.bash
# Verify entry point name in setup.py matches what you're running
```

### Problem: `ImportError: No module named 'drone_delivery_interfaces'`
```bash
# Cause: Interfaces package not built or not sourced
# Fix:
colcon build --packages-select drone_delivery_interfaces
source install/setup.bash
colcon build --packages-select drone_delivery_system
source install/setup.bash
```

### Problem: Service call hangs / times out
```bash
# Cause: Service server not running, or wrong service name
# Fix:
ros2 service list  # Is /takeoff in the list?
ros2 node list     # Is the server node running?
# Check spelling: '/takeoff' vs '/TakeOff' vs 'takeoff'
```

### Problem: Action goal rejected immediately
```bash
# Cause: goal_callback returning REJECT, or wrong action name
# Fix:
ros2 action list   # Is /deliver_package in the list?
# Add debug logging to goal_callback
```

### Problem: Topics not connecting (subscriber gets nothing)
```bash
# Cause: Topic name mismatch (most common!), wrong type
# Fix:
ros2 topic info /battery_status --verbose
# Compare publisher and subscriber topic names CHARACTER BY CHARACTER
# Check message type matches exactly
```

### Problem: `colcon build` fails with CMake error
```bash
# Cause: Missing dependency, wrong CMakeLists.txt
# Fix:
# Check error message — usually says what's missing
sudo apt install ros-jazzy-MISSING-PACKAGE
# Or add to CMakeLists.txt find_package(...)
```

### Problem: Parameters not loading from launch file
```bash
# Cause: Type mismatch in parameters dict
# Fix:
# Float params MUST be float: 15.0 not 15 (int!)
parameters=[{'drone_speed_ms': 15.0}]  # ← Float, not int
```

---

## 12.8 — Q&A Preparation

**Q: Can ROS2 run on Windows?**
> A: Yes, but Ubuntu is strongly recommended for stability. ROS2 Jazzy officially supports Ubuntu 24.04 LTS. Windows builds exist but have limitations.

**Q: Is Python or C++ better for ROS2?**
> A: Python (rclpy) is excellent for learning and rapid prototyping. C++ (rclcpp) offers better performance for computation-heavy tasks. Most production systems use a mix — Python for high-level logic, C++ for sensor drivers and control loops.

**Q: How does this connect to a real drone?**
> A: Replace the simulated nodes (GPS, battery) with real hardware drivers. PX4 + MAVROS provides a ROS2 bridge to real flight controllers. See Part 13 for details.

**Q: What is the difference between `spin()` and `spin_once()`?**
> A: `spin()` runs forever processing callbacks. `spin_once()` processes one callback then returns. Use `spin()` in standalone nodes; `spin_once()` in loops where you need custom control.

**Q: What does QoS mean?**
> A: Quality of Service — settings that control how messages are delivered. Key settings: Reliability (RELIABLE vs BEST_EFFORT), Durability (VOLATILE vs TRANSIENT_LOCAL), History (KEEP_LAST n messages). Critical for real-time robotics.

**Q: Can two nodes publish to the same topic?**
> A: Yes! Multiple publishers on one topic is perfectly valid. Subscribers receive messages from all publishers. Useful for redundancy (two GPS modules), fan-in patterns, and testing.

**Q: What happens if I call `ros2 topic echo` on a topic no one publishes to?**
> A: It waits silently. No error. Just shows "Waiting for messages..."

---

# PART 13 — ADVANCED BONUS & NEXT STEPS

## Where to Go After This Workshop

Congratulations! You now understand the foundation of real robotic systems. Here's your path forward:

---

## 🎮 Gazebo Simulation

**What it is:** Physics-based 3D robot/drone simulator. Simulate a complete drone with physics, sensors, and environments — no real hardware needed.

```bash
# Install Gazebo Harmonic (latest)
sudo apt install ros-jazzy-gz-ros2-control ros-jazzy-ros-gz

# Launch a drone world
ros2 launch drone_description spawn_drone.launch.py
```

Why use it:
- Test dangerous maneuvers safely
- Develop code without hardware
- Simulate sensor failures
- Run hundreds of tests overnight automatically

**Learn:** [gazebosim.org](https://gazebosim.org)

---

## 📊 RViz2 — 3D Visualization

**What it is:** ROS2's built-in 3D visualization tool. Display robot models, sensor data, trajectories, maps in real-time.

```bash
# Launch RViz2
rviz2

# You can visualize:
# - GPS path as a 3D trajectory
# - Drone 3D model moving
# - Sensor coverage area
# - Planned vs. actual flight path
```

For our workshop system, you'd add:
- Path visualization (NavPath message)
- Drone URDF model
- GPS point cloud

---

## 🚁 PX4 — Real Drone Flight Controller

**What it is:** Open-source autopilot firmware running on Pixhawk hardware. Powers thousands of commercial and research drones worldwide.

```
Your ROS2 Code ←──MAVROS──→ PX4 Flight Controller ←─── Hardware
(Mission Logic)              (Safety, Stabilization)     (Motors, GPS, IMU)
```

Key capabilities:
- Position hold, waypoint navigation
- Failsafe behaviors (return to home)
- Sensor fusion (GPS + IMU + barometer)
- Hardware-in-the-loop simulation

**Learn:** [px4.io](https://px4.io) + [MAVROS docs](https://github.com/mavlink/mavros)

---

## 🔗 MAVROS Integration

**What it is:** Bridge between MAVLink protocol (PX4/ArduPilot) and ROS2.

```python
# With MAVROS, you can:
# Arm the drone
ros2 service call /mavros/cmd/arming mavros_msgs/srv/CommandBool "{value: true}"

# Set flight mode
ros2 service call /mavros/set_mode mavros_msgs/srv/SetMode "{custom_mode: 'OFFBOARD'}"

# Send position commands
from geometry_msgs.msg import PoseStamped
# Publish to /mavros/setpoint_position/local
```

**Learn:** [github.com/mavlink/mavros](https://github.com/mavlink/mavros)

---

## 🗺️ Navigation Stack (Nav2)

**What it is:** ROS2's complete autonomous navigation system. Originally for ground robots, adapted for drones.

Capabilities:
- Global path planning (A*, Dijkstra)
- Local obstacle avoidance (DWA planner)
- Costmaps (occupancy grids)
- Behavior trees for complex missions
- Recovery behaviors

```
Your Drone → Nav2 Stack → Waypoints → MAVROS → PX4 → Motors
           ← Costmaps ← SLAM ← Camera/LiDAR
```

**Learn:** [navigation.ros.org](https://navigation.ros.org)

---

## 🗺️ SLAM (Simultaneous Localization and Mapping)

**What it is:** Build a map of unknown environment while tracking position within it.

Popular ROS2 SLAM packages:
- **RTAB-Map** — RGB-D SLAM (camera + depth)
- **SLAM Toolbox** — 2D LiDAR SLAM
- **Cartographer** — Google's SLAM (2D/3D)
- **ORB-SLAM3** — Visual SLAM (camera only)

```bash
# Install SLAM Toolbox
sudo apt install ros-jazzy-slam-toolbox

# Launch for drone mapping
ros2 launch slam_toolbox online_async_launch.py
```

---

## 👁️ Computer Vision

**What it is:** Give your drone the ability to see and understand the world.

With ROS2 + OpenCV:
- Object detection for landing zones
- Package recognition at delivery site
- Obstacle detection and avoidance
- ArUco marker tracking for precision landing

```python
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.bridge = CvBridge()
        self.image_sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10
        )
    
    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        # Run your CV algorithms here
        # ... ArUco detection, YOLO, etc.
```

---

## 🤖 Complete Autonomous Drone Stack

When you're ready to build a production-level autonomous drone:

```
┌─────────────────────────────────────────────────────────┐
│              FULL AUTONOMOUS DRONE STACK                │
│                                                         │
│  Mission Planner (your code from today)                 │
│       ↓                                                 │
│  Navigation (Nav2)                                      │
│       ↓                                                 │
│  SLAM (mapping + localization)                          │
│       ↓                                                 │
│  MAVROS bridge                                          │
│       ↓                                                 │
│  PX4 flight controller                                  │
│       ↓                                                 │
│  Physical motors/props/sensors                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📚 Recommended Learning Path

| Week | Topic | Resource |
|------|-------|----------|
| 1–2 | ROS2 fundamentals (this workshop!) | Done! ✅ |
| 3–4 | Gazebo simulation | [gazebosim.org/docs](https://gazebosim.org/docs) |
| 5–6 | Nav2 navigation stack | [navigation.ros.org](https://navigation.ros.org) |
| 7–8 | PX4 + MAVROS | [px4.io/docs](https://docs.px4.io) |
| 9–10 | SLAM + mapping | [slam-toolbox docs](https://github.com/SteveMacenski/slam_toolbox) |
| 11–12 | Computer vision | [OpenCV + ROS2 tutorial](https://docs.opencv.org) |
| 13+ | Real hardware | Start with simulation → then real drone |

---

## 🏆 Final Project Ideas

After the workshop, challenge yourself with these projects:

1. **Multi-Drone Coordination** — Two drones, one monitors the other. If drone 1's battery is low, drone 2 takes over the delivery.

2. **Emergency Return** — Monitor battery + wind speed. If wind > 15 m/s OR battery < 25%, automatically trigger return-to-home action.

3. **Delivery Queue System** — Service that accepts multiple delivery requests, queues them, and sends them one by one as the drone completes each mission.

4. **Real GPS Map Integration** — Use actual OpenStreetMap data to visualize the drone path in RViz2 with real-world coordinates.

5. **Fleet Management Dashboard** — Manage 5 simulated drones, each with their own topics and actions, unified into one ground control dashboard.

---

## 🎓 Certification and Community

- **ROS2 Robotics Developer** certification: [The Construct](https://www.theconstructsim.com)
- **Aerial Robotics** on Coursera (University of Pennsylvania)
- **ROS Discourse** community: [discourse.ros.org](https://discourse.ros.org)
- **ROS2 GitHub**: [github.com/ros2](https://github.com/ros2)
- **ROSCon** — Annual conference, talks available free online

---

## Final Architecture Review

```
╔══════════════════════════════════════════════════════════════╗
║          DRONE DELIVERY SYSTEM — COMPLETE ARCHITECTURE       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  PUBLISHERS              TOPICS              SUBSCRIBERS     ║
║  ─────────               ──────              ───────────     ║
║  gps_node          →  /gps_location    →  ground_control    ║
║  battery_monitor   →  /battery_status  →  ground_control    ║
║  drone_status      →  /drone_status    →  ground_control    ║
║  delivery_server   →  /drone_state_cmd →  drone_status      ║
║  takeoff_server    →  /drone_state_cmd →  drone_status      ║
║                                                              ║
║  CLIENTS                SERVICES            SERVERS          ║
║  ───────                ────────            ───────          ║
║  ground_control    →  /takeoff         →  takeoff_server    ║
║  ground_control    →  /land            →  takeoff_server    ║
║  ground_control    →  /change_dest     →  dest_server       ║
║                                                              ║
║  ACTION CLIENTS         ACTIONS             ACTION SERVERS   ║
║  ──────────────         ───────             ─────────────   ║
║  delivery_client   →  /deliver_pkg     →  delivery_server   ║
║                    ←  [feedback]       ←                     ║
║                    ←  [result]         ←                     ║
║                                                              ║
║  PARAMETERS (all configurable live with ros2 param set)     ║
║  ──────────────────────────────────────────────────────     ║
║  /battery_monitor_node:                                      ║
║    battery_warning_threshold   (default: 20.0)              ║
║    discharge_rate              (default: 0.5)               ║
║    initial_battery             (default: 100.0)             ║
║  /gps_node:                                                  ║
║    home_latitude               (default: 23.5880)           ║
║    home_longitude              (default: 58.3829)           ║
║    home_altitude               (default: 50.0)              ║
║  /delivery_action_server:                                    ║
║    drone_speed_ms              (default: 15.0)              ║
║    max_altitude                (default: 120.0)             ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🚁 Congratulations!

You have built a **complete, professional ROS2 drone delivery system** from scratch. You now understand:

✅ **ROS2 Workspaces** — Create, build, and source  
✅ **Packages** — Python and CMake packages, dependencies  
✅ **Nodes** — rclpy.init, Node class, spin(), timers  
✅ **Topics** — Publishers, subscribers, callbacks, message types  
✅ **Services** — Request/response, server/client, Trigger and custom services  
✅ **Actions** — Goals, feedback, results, cancellation, MultiThreadedExecutor  
✅ **Parameters** — Declare, read, set live, callbacks  
✅ **Launch Files** — LaunchDescription, arguments, multiple nodes  
✅ **Debugging** — rqt_graph, ros2 doctor, topic echo, param list  
✅ **Architecture** — How real-world robotic systems are structured  

*The skills you learned today are the same skills used by robotics engineers at*  
*Amazon, DJI, Boston Dynamics, NASA, and hundreds of robotics startups worldwide.*

**🚀 Now go build something incredible!**

---

*Workshop created for ROS2 Jazzy Jalisco*  
*Ubuntu 24.04 LTS | Python 3.12 | rclpy*  
*© 2024 Drone Delivery Workshop — Free to use and share*
