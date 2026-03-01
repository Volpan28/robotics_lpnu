# Laboratory Work 2: ROS2 Integration with Gazebo

## Overview
This repository contains the solution for Lab 2. It demonstrates the integration of a custom 4-wheeled mobile robot (created in Lab 1) with ROS2. The package includes nodes for controlling the robot's movement via velocity commands and processing LiDAR sensor data for obstacle detection.

## Prerequisites
- Ubuntu (native or WSL2)
- Docker installed and configured

---

## Quick Start Guide

### Step 1: Start the Environment
Open your terminal in the root directory of this repository and start the Docker container:

```bash
# Start and enter the Docker container
./scripts/cmd run
```
(Keep this terminal open - this will be your main workspace)

### Step 2: Build the Package
Inside the container, compile the lab2 package and source the workspace:

```bash
cd /opt/ws
colcon build --packages-select lab2
source install/setup.bash
```

### Step 3: Launch Simulation and Bridge (Terminal 1)
Launch Gazebo, RViz2, and the ros_gz_bridge simultaneously using the provided launch file:

```bash
ros2 launch lab2 gazebo_ros2.launch.py
```

Important: Ensure the Gazebo simulation is playing. Press the play button in the bottom left corner of the Gazebo GUI if it starts paused.

### Step 4: Run the Robot Controller (Terminal 2)
Open a new terminal, enter the container, source the workspace, and start the publisher node to move the robot:

```bash
./scripts/cmd bash
source /opt/ws/install/setup.bash
ros2 run lab2 robot_controller
```

The robot will start moving forward in a sinusoidal path.

### Step 5: Run the LiDAR Subscriber (Terminal 3)
Open a third terminal, enter the container, source the workspace, and start the subscriber node to process sensor data:

```bash
./scripts/cmd bash
source /opt/ws/install/setup.bash
ros2 run lab2 lidar_subscriber
```

Watch the console output. If the robot approaches an obstacle closer than 1.0 meter, a yellow [WARN] message will appear indicating an obstacle detection.

