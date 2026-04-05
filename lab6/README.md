# Laboratory Work 6: Motion Planning for Mobile Robots (Nav2)

## Overview
This repository contains the completed Laboratory Work 6. The official ROS 2 Navigation Stack (**Nav2**) was utilized to enable autonomous point-to-point navigation for the TurtleBot3 within a mapped environment. The core task involved tuning intentionally poor default parameters to achieve smooth and reliable motion planning.

## Quick Start Guide

### Step 1: Build the Workspace
Ensure both `lab3` (contains the world with obstacles) and `lab6` are built:

```bash
cd /opt/ws
colcon build --packages-select lab3 lab6
source install/setup.bash
```

### Step 2: Launch Simulation & Nav2
Launch Gazebo, RViz2, and the Nav2 stack components:

```bash
ros2 launch lab6 nav2_room_bringup.launch.py
```

### Step 3: Navigate via RViz2
- Localization: Select 2D Pose Estimate in the top toolbar of RViz2. Click and drag on the map where the robot is currently spawned in Gazebo to initialize the AMCL algorithm.

- Navigation: Select Nav2 Goal in the toolbar. Click and drag in a clear area on the map to set the destination and final orientation.

## Parameter Tuning (Task 2)
The default lab6/config/nav2_params.yaml file was modified to improve the robot's performance:

1. Goal Checker (xy_goal_tolerance reduced from 0.75 to 0.20): Ensured the robot stops precisely at the target rather than triggering a premature "Goal reached" state.

2. Local Costmap (update_frequency increased from 2.0 to 5.0): Eliminated costmap blur and drift during rapid rotations by processing LiDAR data faster.

3. Controller Server (max_vel_theta reduced from 2.5 to 1.0): Smoothed out rotational movements, preventing wobbling near walls and obstacles.

### Concepts Explored
- Global Planner: Uses the static saved map to compute the optimal, collision-free path to the destination.

- Local Controller: Uses real-time LiDAR data (Local Costmap) to follow the global path while dynamically avoiding new or unmapped obstacles.

