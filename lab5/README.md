# Laboratory Work 5: Obstacle Avoidance

## Overview
This repository contains the solution for Lab 5. It implements an **Artificial Potential Fields (APF)** algorithm to navigate a TurtleBot3 robot from a starting position to a designated goal while dynamically avoiding obstacles using LiDAR sensor data.

## Quick Start Guide

### Step 1: Build the Workspace
Ensure both `lab3` (contains the world with obstacles) and `lab5` are built:

```bash
cd /opt/ws
colcon build --packages-select lab3 lab5
source install/setup.bash
```

### Step 2: Launch Simulation (Terminal 1)
Launch the Gazebo room environment containing the TurtleBot3 and the added obstacles (red box, blue and green cylinders), along with RViz2:

```bash
ros2 launch lab5 obstacle_avoidance_bringup.launch.py
```

### Step 3: Run the APF Algorithm (Terminal 2)
In a new terminal, run the avoidance node. You can specify the goal coordinates using ROS 2 parameters:

```bash
source /opt/ws/install/setup.bash
ros2 run lab5 obstacle_avoidance --ros-args -p goal_x:=2.5 -p goal_y:=2.5
```

### Implementation Details
- Algorithm: Artificial Potential Fields.

- Inputs: * /odom (Odometry) to determine the robot's current pose and distance to the goal.

- /scan (LaserScan) to detect obstacles and calculate repulsive forces.

- Outputs: /cmd_vel (Twist) to drive the robot.

- Logic: The robot calculates an attractive force vector towards the (goal_x, goal_y) and a repulsive force vector away from any LiDAR points closer than safe_dist. These vectors are summed to produce linear and angular velocity commands.

### Known Issues (Algorithm Limitations)
During testing, the classic "Local Minimum" issue of the APF algorithm was observed. When obstacles are placed close together, their combined repulsive fields can counteract the attractive field of the goal. This sometimes causes the robot to take wide detours, turn around entirely, or get temporarily stuck in an oscillating state before finding a clear path.