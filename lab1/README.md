# Laboratory Work 1: Building a Robot in Gazebo

## Overview
This repository contains the solution for Lab 1. It features a custom 4-wheeled mobile robot equipped with a differential drive controller and a LiDAR sensor, navigating a simulated environment with test obstacles.

## Prerequisites
- Ubuntu (native or WSL2)
- Docker installed and configured

---

## Quick Start Guide

### Step 1: Build and Start the Environment
Open your terminal in the root directory of this repository and execute the following commands to set up the Docker container:

```bash
# Build the Docker image (only needed the first time)
./scripts/cmd build-docker

# Start and enter the Docker container
./scripts/cmd run
```

### Step 2: Launch the Gazebo Simulation
Inside the running container (in Terminal 1), start the simulation with our custom robot world:

```bash
gz sim /opt/ws/src/code/lab1/worlds/robot.sdf
```

## Important: 
Ensure the simulation is playing. If it starts paused, press the Play button in the bottom left corner of the Gazebo GUI.

### Step 3: Control the Robot
You can control the robot's movement using terminal commands. Open a new terminal (Terminal 2), navigate to the repository root, and enter the container:

```bash
./scripts/cmd bash
```

Send a movement command to drive the robot forward:

```bash
gz topic -t "/cmd_vel" -m gz.msgs.Twist -p "linear: {x: 0.5}, angular: {z: 0.0}"
```

To stop the robot, send zero velocity:

```bash
gz topic -t "/cmd_vel" -m gz.msgs.Twist -p "linear: {x: 0.0}, angular: {z: 0.0}"
```

## Tip: You can also use the Teleop plugin inside the Gazebo GUI. Set the topic to /cmd_vel and use your keyboard arrows to drive the robot.

### Step 4: Verify LiDAR Sensor Data
To verify that the LiDAR is scanning the obstacles, open a third terminal, enter the container (./scripts/cmd bash), and read the live data stream:

```bash
gz topic -e -t /lidar
```
Press Ctrl+C to stop the data stream.

## Tip: In the Gazebo GUI, you can activate the Visualize Lidar plugin and select the /lidar topic from the dropdown menu to see the blue laser rays interacting with the environment.