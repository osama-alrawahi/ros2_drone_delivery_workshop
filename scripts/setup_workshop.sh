#!/usr/bin/env bash
# =============================================================================
# ROS2 Drone Delivery Workshop — Automated Setup Script
# =============================================================================
# Usage:
#   cd ~/ros2_ws/src/ros2_drone_delivery_workshop
#   chmod +x scripts/setup_workshop.sh
#   ./scripts/setup_workshop.sh
#
# What this script does:
#   1. Checks that ROS2 Jazzy is installed
#   2. Sources ROS2 environment
#   3. Moves packages to the correct workspace location
#   4. Builds drone_delivery_interfaces first (required by main package)
#   5. Builds drone_delivery_system
#   6. Sources the new install
#   7. Verifies everything works
# =============================================================================

set -e  # Exit immediately on any error

# ── Colours ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'   # No Colour

# ── Helpers ───────────────────────────────────────────────────────────────────
info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }
step()    { echo -e "\n${BOLD}${CYAN}▶ $*${NC}"; }

# =============================================================================
echo ""
echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${CYAN}║   🚁  ROS2 Drone Delivery Workshop — Setup Script        ║${NC}"
echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# =============================================================================
# STEP 1: Check ROS2 Jazzy is installed
# =============================================================================
step "Step 1/6 — Checking ROS2 Jazzy installation..."

if [ ! -f "/opt/ros/jazzy/setup.bash" ]; then
    error "ROS2 Jazzy not found at /opt/ros/jazzy/setup.bash\n\
       Please install ROS2 Jazzy first:\n\
       https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html"
fi
success "ROS2 Jazzy found at /opt/ros/jazzy"

# Source ROS2
source /opt/ros/jazzy/setup.bash
success "ROS2 Jazzy sourced"

# =============================================================================
# STEP 2: Locate workspace
# =============================================================================
step "Step 2/6 — Locating ROS2 workspace..."

# Determine the workspace root — this script lives in:
#   ~/ros2_ws/src/ros2_drone_delivery_workshop/scripts/setup_workshop.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$(cd "$REPO_DIR/.." && pwd)"
WS_DIR="$(cd "$SRC_DIR/.." && pwd)"

info "Repository   : $REPO_DIR"
info "Workspace src: $SRC_DIR"
info "Workspace    : $WS_DIR"

# Validate this looks like a ROS2 workspace
if [ ! -d "$WS_DIR/src" ]; then
    error "Could not find workspace/src directory.\n\
       Make sure you cloned into ~/ros2_ws/src/\n\
       Expected structure:\n\
         ~/ros2_ws/src/ros2_drone_delivery_workshop/"
fi
success "Workspace structure looks correct"

# =============================================================================
# STEP 3: Install system dependencies
# =============================================================================
step "Step 3/6 — Checking system dependencies..."

MISSING_DEPS=()

# Check colcon
if ! command -v colcon &>/dev/null; then
    MISSING_DEPS+=("python3-colcon-common-extensions")
fi

# Check required ROS2 packages
for pkg in ros-jazzy-std-msgs ros-jazzy-sensor-msgs ros-jazzy-std-srvs \
           ros-jazzy-action-msgs ros-jazzy-rosidl-default-generators; do
    if ! dpkg -l "$pkg" &>/dev/null 2>&1; then
        MISSING_DEPS+=("$pkg")
    fi
done

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    warn "Missing packages detected. Installing..."
    warn "You may be prompted for your sudo password."
    sudo apt-get update -qq
    sudo apt-get install -y "${MISSING_DEPS[@]}"
    success "Dependencies installed"
else
    success "All dependencies already installed"
fi

# =============================================================================
# STEP 4: Build interfaces package first
# =============================================================================
step "Step 4/6 — Building drone_delivery_interfaces..."
info "This must be built first — the main package depends on it"

cd "$WS_DIR"

if colcon build \
    --packages-select drone_delivery_interfaces \
    --symlink-install \
    2>&1 | tee /tmp/interfaces_build.log | grep -E "ERROR|error|Finished|Starting|Summary"; then
    success "drone_delivery_interfaces built successfully"
else
    error "Build failed. Full log: /tmp/interfaces_build.log"
fi

# Source after build
source "$WS_DIR/install/setup.bash"

# Verify interfaces
info "Verifying custom interfaces..."
if ros2 interface show drone_delivery_interfaces/srv/ChangeDestination &>/dev/null; then
    success "ChangeDestination service interface: OK"
else
    error "Interface verification failed. Check build output."
fi

if ros2 interface show drone_delivery_interfaces/action/DeliverPackage &>/dev/null; then
    success "DeliverPackage action interface: OK"
else
    error "Interface verification failed. Check build output."
fi

# =============================================================================
# STEP 5: Build main package
# =============================================================================
step "Step 5/6 — Building drone_delivery_system..."

if colcon build \
    --packages-select drone_delivery_system \
    --symlink-install \
    2>&1 | tee /tmp/main_build.log | grep -E "ERROR|error|Finished|Starting|Summary"; then
    success "drone_delivery_system built successfully"
else
    error "Build failed. Full log: /tmp/main_build.log"
fi

source "$WS_DIR/install/setup.bash"

# =============================================================================
# STEP 6: Verify all executables
# =============================================================================
step "Step 6/6 — Verifying node executables..."

NODES=(
    "drone_status_node"
    "battery_monitor_node"
    "gps_node"
    "ground_control_node"
    "takeoff_service_server"
    "takeoff_service_client"
    "destination_service_server"
    "destination_service_client"
    "delivery_action_server"
    "delivery_action_client"
)

ALL_OK=true
INSTALL_LIB="$WS_DIR/install/drone_delivery_system/lib/drone_delivery_system"

for node in "${NODES[@]}"; do
    # Fast check: just verify the executable file exists — no need to launch it
    if [ -f "$INSTALL_LIB/$node" ]; then
        success "  ✓ $node"
    else
        warn "  ✗ $node — not found in $INSTALL_LIB"
        ALL_OK=false
    fi
done

if [ "$ALL_OK" = false ]; then
    warn "Some executables missing. Try: colcon build --packages-select drone_delivery_system"
fi

# =============================================================================
# DONE — Print instructions
# =============================================================================
echo ""
echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${GREEN}║   ✅  Setup Complete! Workshop is ready.                  ║${NC}"
echo -e "${BOLD}${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BOLD}IMPORTANT: Run this in EVERY new terminal:${NC}"
echo -e "  ${CYAN}source ~/ros2_ws/install/setup.bash${NC}"
echo ""
echo -e "${BOLD}Or add it permanently (one-time):${NC}"
echo -e "  ${CYAN}echo 'source ~/ros2_ws/install/setup.bash' >> ~/.bashrc${NC}"
echo ""
echo -e "${BOLD}Quick start commands:${NC}"
echo ""
echo -e "  ${YELLOW}# Launch all nodes at once${NC}"
echo -e "  ${CYAN}ros2 launch drone_delivery_system drone_delivery.launch.py${NC}"
echo ""
echo -e "  ${YELLOW}# In a second terminal — take off${NC}"
echo -e "  ${CYAN}ros2 service call /takeoff std_srvs/srv/Trigger {}${NC}"
echo ""
echo -e "  ${YELLOW}# Start a delivery mission with live feedback${NC}"
echo -e "  ${CYAN}ros2 action send_goal /deliver_package \\"
echo -e "    drone_delivery_interfaces/action/DeliverPackage \\"
echo -e "    \"{package_id: 'PKG-001', destination_name: 'SQU',${NC}"
echo -e "  ${CYAN}     target_latitude: 23.6097, target_longitude: 58.1804,${NC}"
echo -e "  ${CYAN}     max_speed: 15.0}\" --feedback${NC}"
echo ""
echo -e "  ${YELLOW}# Watch the node graph visually${NC}"
echo -e "  ${CYAN}rqt_graph${NC}"
echo ""
echo -e "${BOLD}Workshop guide:${NC}  docs/ros2_drone_delivery_workshop.md"
echo ""

# Offer to add source to .bashrc
read -rp "Add 'source ~/ros2_ws/install/setup.bash' to ~/.bashrc automatically? [Y/n]: " answer
if [[ "$answer" =~ ^[Yy]$|^$ ]]; then
    if ! grep -q "source ~/ros2_ws/install/setup.bash" ~/.bashrc; then
        {
            echo ""
            echo "# ROS2 Drone Delivery Workshop — auto-added by setup_workshop.sh"
            echo "source /opt/ros/jazzy/setup.bash"
            echo "source ~/ros2_ws/install/setup.bash"
        } >> ~/.bashrc
        success "Added to ~/.bashrc — restart terminal or run: source ~/.bashrc"
    else
        info "Already in ~/.bashrc — no change needed"
    fi
fi

echo ""
success "Ready to fly! 🚁"
echo ""
