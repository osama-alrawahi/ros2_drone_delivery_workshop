# 🚁 ROS2 Drone Delivery System — Workshop

> **Complete beginner ROS2 workshop** — Build a real autonomous drone delivery system from scratch.

[![ROS2 Jazzy](https://img.shields.io/badge/ROS2-Jazzy-blue)](https://docs.ros.org/en/jazzy/)
[![Ubuntu 24.04](https://img.shields.io/badge/Ubuntu-24.04-orange)](https://ubuntu.com/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-green)](https://python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellow)](LICENSE)

---

## ⚡ Quick Start — One Command Setup

```bash
# 1. Clone the repo into your ROS2 workspace
cd ~/ros2_ws/src
git clone https://github.com/osama-alrawahi/ros2_drone_delivery_workshop.git

# 2. Run the automated setup script
cd ~/ros2_ws/src/ros2_drone_delivery_workshop
chmod +x scripts/setup_workshop.sh
./scripts/setup_workshop.sh
```

That's it. The script builds everything and you're ready to go.

---

## 📦 Packages in this Repo

| Package | Type | Description |
|---------|------|-------------|
| `drone_delivery_interfaces` | CMake | Custom `.srv` and `.action` definitions |
| `drone_delivery_system` | Python | All 10 ROS2 nodes + launch file |

---

## 🚀 Run the Complete System

```bash
source ~/ros2_ws/install/setup.bash

# Launch ALL nodes at once
ros2 launch drone_delivery_system drone_delivery.launch.py

# Launch with custom parameters
ros2 launch drone_delivery_system drone_delivery.launch.py \
  drone_speed:=20.0 battery_warning:=25.0
```

---

## 🎮 Interactive Commands (in a new terminal)

```bash
source ~/ros2_ws/install/setup.bash

# Command drone to take off
ros2 service call /takeoff std_srvs/srv/Trigger {}

# Change delivery destination
ros2 service call /change_destination \
  drone_delivery_interfaces/srv/ChangeDestination \
  "{latitude: 23.6097, longitude: 58.1804, destination_name: 'SQU'}"

# Send full delivery mission with live feedback
ros2 action send_goal /deliver_package \
  drone_delivery_interfaces/action/DeliverPackage \
  "{package_id: 'PKG-001', destination_name: 'SQU', \
    target_latitude: 23.6097, target_longitude: 58.1804, max_speed: 15.0}" \
  --feedback

# View live battery
ros2 topic echo /battery_status

# See all node connections (GUI)
rqt_graph
```

---

## 🗂️ Node Reference

| Node | Executable | Topics | Services | Actions |
|------|-----------|--------|----------|---------|
| Drone Status | `drone_status_node` | pub `/drone_status` | — | — |
| Battery Monitor | `battery_monitor_node` | pub `/battery_status` | — | — |
| GPS | `gps_node` | pub `/gps_location` | — | — |
| Ground Control | `ground_control_node` | sub all telemetry | — | — |
| Takeoff Server | `takeoff_service_server` | — | `/takeoff`, `/land` | — |
| Destination Server | `destination_service_server` | — | `/change_destination` | — |
| Delivery Server | `delivery_action_server` | — | — | `/deliver_package` |

---

## 📚 Workshop Parts

| Part | Topic |
|------|-------|
| 1 | Introduction to ROS2 |
| 2 | Create ROS2 Workspace |
| 3 | Create Packages |
| 4 | Create Nodes |
| 5 | Topics (Publisher/Subscriber) |
| 6 | Services |
| 7 | Actions |
| 8 | Parameters |
| 9 | Launch Files |
| 10 | Visualization & Debugging |
| 11 | Final Integrated Demo |
| 12 | Workshop Materials & Exercises |
| 13 | Advanced Bonus & Next Steps |

---

## 🛠️ Manual Setup (if script fails)

```bash
cd ~/ros2_ws

# Build interfaces first (required dependency)
colcon build --packages-select drone_delivery_interfaces
source install/setup.bash

# Then build the main package
colcon build --packages-select drone_delivery_system
source install/setup.bash
```

---

## ✅ Verify Installation

```bash
source ~/ros2_ws/install/setup.bash

# Check interfaces exist
ros2 interface show drone_delivery_interfaces/srv/ChangeDestination
ros2 interface show drone_delivery_interfaces/action/DeliverPackage

# Check executables exist
ros2 run drone_delivery_system --help
```

---

## 📋 Requirements

- Ubuntu 24.04 LTS
- ROS2 Jazzy Jalisco ([installation guide](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html))
- Python 3.12+
- colcon build tools: `sudo apt install python3-colcon-common-extensions`

---

## 🏫 For Instructors

The full workshop document (all 13 parts with explanations, code, exercises, quiz, cheat sheet) is in:
```
docs/ros2_drone_delivery_workshop.md
```

Each node file is **heavily commented** — designed to be read line by line in a workshop setting.

---

## 📁 Repository Structure

```
ros2_drone_delivery_workshop/
├── README.md
├── LICENSE
├── .gitignore
├── scripts/
│   └── setup_workshop.sh           ← One-command installer
├── docs/
│   └── ros2_drone_delivery_workshop.md  ← Full workshop guide
├── drone_delivery_interfaces/      ← Custom message definitions
│   ├── package.xml
│   ├── CMakeLists.txt
│   ├── srv/
│   │   └── ChangeDestination.srv
│   └── action/
│       └── DeliverPackage.action
└── drone_delivery_system/          ← All Python nodes
    ├── package.xml
    ├── setup.py
    ├── setup.cfg
    ├── resource/
    │   └── drone_delivery_system
    ├── launch/
    │   └── drone_delivery.launch.py
    └── drone_delivery_system/
        ├── __init__.py
        ├── drone_status_node.py
        ├── battery_monitor_node.py
        ├── gps_node.py
        ├── ground_control_node.py
        ├── takeoff_service_server.py
        ├── takeoff_service_client.py
        ├── destination_service_server.py
        ├── destination_service_client.py
        ├── delivery_action_server.py
        └── delivery_action_client.py
```

---

## 🤝 Contributing

Pull requests welcome! If you build something cool on top of this workshop, open an issue and share it.

---

*Built for ROS2 Jazzy | Ubuntu 24.04 | Workshop use permitted freely*
