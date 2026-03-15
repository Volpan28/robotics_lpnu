# Laboratory Work 3: Path Following and Trajectory Control

## Overview
This repository contains the solution for Lab 3. It explores differential drive kinematics and trajectory control in ROS2 and Gazebo. The lab includes executing predefined paths (square, circle) and a custom implemented figure-8 trajectory. It also introduces the standard **TurtleBot3** robot in a simulated room environment.

## Quick Start Guide

### Step 1: Start the Environment
Open your terminal in the root directory and start the Docker container:

```bash
./scripts/cmd run
```

### Step 2: Build the Workspace
Inside the container, compile the lab3 package and source the workspace:

```bash
cd /opt/ws
colcon build --packages-select lab3
source install/setup.bash
```
### Step 3: Launch Simulation (Terminal 1)
Launch the Gazebo room environment with TurtleBot3 and RViz2 for visualization:

```bash
ros2 launch lab3 turtlebot3_room_bringup.launch.py
```

### Step 4: Run Trajectories (Terminal 2)
Open a new terminal, enter the container (./scripts/cmd bash), source the setup file, and run one of the desired paths:

#### 1. Square Path (using Odometry):

```bash
source /opt/ws/install/setup.bash
ros2 run lab3 square_path --ros-args -p odom_topic:=/odom
```

#### 2. Figure-8 Path (Custom Implementation):
Runs a timed sequence of two circles. Slower speeds and a time multiplier (e.g., 1.37) are used to compensate for Gazebo's Real-Time Factor (RTF) physics delays and motor limits:

```bash
source /opt/ws/install/setup.bash
ros2 run lab3 figure_8_path --ros-args -p linear_speed:=0.15 -p angular_speed:=0.3
```

## Key Implementations
- figure_8_path.py: A custom ROS2 node that publishes TwistStamped messages to /cmd_vel to draw a figure-8 shape. It handles physical motor limitations and compensates for simulation time delays (RTF < 1.0).

- RViz2 Trajectory Tracking: The odom_path_publisher node translates odometry data into a Path message, allowing real-time trajectory drawing in RViz2.

## Troubleshooting
- Robot does not move ("Waiting for odometry..."): Ensure you are passing the correct odometry topic for TurtleBot3 (--ros-args -p odom_topic:=/odom).

- Console spam TF_OLD_DATA: This happens when restarting the Gazebo simulation while RViz2 is still open. Click the "Reset" button in the bottom left corner of the RViz2 window.

- Robot disappears or flies away: The robot likely hit a wall at high speed, breaking the physics engine. Restart the ros2 launch command.