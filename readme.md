
# Avatar Challenge 

## Features

- Load shapes from YAML configuration
- Generate interpolated Cartesian trajectories
- Execute trajectory with MoveIt2
- Visualize trajectory in RViz
---

## Requirements
- pymoveit2

Install required packages:

```bash

pip install pymoveit2

```

Project Structure
```
avatar_challenge
├── avatar_challenge
│   └── shapes_loader.py
├── config
│   └── shapes.yaml
├── launch
│   └── demo.launch.py
├── package.xml
├── setup.py
└── README.md
```

Shape Configuration

Shapes are defined in:

```
config/shapes.yaml

Example:

shapes:
  - num: 4
    start_pose:
      position: [0.4, 0.0, 0.2]
      rpy: [0, 0, 0]
    vertices:
      - [0,0]
      - [0.1,0]
      - [0.1,0.1]
      - [0,0.1]
```

Launch the system:
```
ros2 launch avatar_challenge demo.launch.py
```


Visualization

Trajectory is published as a ROS marker:
```
/trajectory_marker
```

Pipeline:
```
shapes.yaml
     ↓
load shapes
     ↓
pose transformation
     ↓
trajectory interpolation
     ↓
MoveIt2 execution
     ↓
RViz visualization
```

Author

Wei Wang


---

# 再给你 3 个 README 提升建议（很重要）

### 1 加一张效果图

README 最好有：


RViz screenshot


GitHub 项目点击率会高很多。

---

### 2 加 architecture 图

例如：


Shapes.yaml
↓
ShapesLoader Node
↓
MoveIt2
↓
ros2_control
↓
Robot


---

### 3 加 quick start（最重要）

很多人只看这一段：

```bash
git clone ...
colcon build
ros2 launch ...
如果你愿意，我可以帮你把 README 升级成 GitHub 展示级别版本，包括：

项目结构图

轨迹动画 gif

系统架构图

RViz 结果图

看起来会像一个 正式机器人项目仓库。

我要完整的readme 内容

下面是一份完整、专业、可以直接放进 README.md 的版本。结构按照常见的 ROS2 + MoveIt 项目规范组织，别人 clone 之后基本可以直接理解和运行你的项目。

Avatar Challenge – Shape Drawing with MoveIt2

This project demonstrates how to generate and execute geometric drawing trajectories using a 7-DOF robotic arm in ROS2.
Shapes are defined in a YAML configuration file, converted into Cartesian waypoints, interpolated into smooth trajectories, and executed using MoveIt2.

The generated trajectory is also visualized in RViz.

Overview

The system reads shape definitions from a configuration file and converts them into a robot end-effector trajectory.

Pipeline:

shapes.yaml
     ↓
Shape Loader Node
     ↓
Pose Transformation
     ↓
Waypoint Interpolation
     ↓
MoveIt2 Motion Planning
     ↓
ros2_control Execution
     ↓
RViz Trajectory Visualization
Features

Load geometric shapes from YAML

Transform shapes into world coordinates

Generate interpolated Cartesian trajectories

Execute trajectories with MoveIt2

Visualize trajectory in RViz

Compatible with xArm7 robot

Requirements

The system is developed and tested with:

ROS2 Humble

MoveIt2

pymoveit2

ros2_control

RViz2

Required packages:

ros-humble-moveit
ros-humble-joint-trajectory-controller
ros-humble-ros2-control
ros-humble-ros2-controllers

Install dependencies:

sudo apt update

sudo apt install ros-humble-moveit
sudo apt install ros-humble-joint-trajectory-controller
sudo apt install ros-humble-ros2-control
sudo apt install ros-humble-ros2-controllers

Install pymoveit2:

pip install pymoveit2
Workspace Setup

Create a ROS2 workspace:

mkdir -p ~/dev_ws/src
cd ~/dev_ws/src

Clone the repository:

git clone <repository_url>

Build the workspace:

cd ~/dev_ws
colcon build --symlink-install

Source the workspace:

source install/setup.bash
Project Structure
avatar_challenge
│
├── avatar_challenge
│   └── shapes_loader.py
│
├── config
│   └── shapes.yaml
│
├── launch
│   └── demo.launch.py
│
├── resource
│
├── package.xml
├── setup.py
└── README.md

Description of important files:

File	Description
shapes_loader.py	ROS2 node for loading shapes and executing trajectories
shapes.yaml	shape definitions
demo.launch.py	launch file starting the system
package.xml	ROS2 package configuration
setup.py	Python package setup
Shape Configuration

Shapes are defined in:

config/shapes.yaml

Example configuration:

shapes:
  - num: 4

    start_pose:
      position: [0.4, 0.0, 0.2]
      rpy: [0.0, 0.0, 0.0]

    vertices:
      - [0.0, 0.0]
      - [0.1, 0.0]
      - [0.1, 0.1]
      - [0.0, 0.1]

Parameter description:

Parameter	Description
num	number of vertices
start_pose	world coordinate of the shape origin
vertices	2D coordinates of shape points

Vertices are defined in the local coordinate frame and then transformed into the world frame.

Running the Demo

Start the system:

ros2 launch avatar_challenge demo.launch.py

This launch file will start:

MoveIt2 motion planning

ros2_control controllers

RViz visualization

shape_loader node

The robot will follow the trajectory defined in the YAML configuration.

Visualization in RViz

The trajectory is published as a marker:

/trajectory_marker

To display the trajectory:

Open RViz

Click Add

Select Marker

Set topic to:

/trajectory_marker

The robot trajectory will appear as a red line in RViz.

Node Description
shape_loader

ROS2 node responsible for:

reading shape configuration

generating interpolated waypoints

sending trajectory commands to MoveIt2

publishing trajectory markers

Main functions:

Function	Description
load_shapes()	load shapes from YAML
interpolation()	generate intermediate points
plan_shapes()	execute trajectory
Trajectory Generation

For each pair of shape vertices:

Convert local vertices into world coordinates

Generate interpolated waypoints

Send waypoint sequence to MoveIt2

Wait for execution

Publish visualization marker

Interpolation uses linear interpolation between points.

Logging

All node logs use the prefix:

[WW]

Example:

[WW] Shape Loader node started
[WW] Loading shapes.yaml
[WW] Generating interpolated waypoints
Example Result

When running the system:

Robot follows the shape trajectory

RViz displays the trajectory

Waypoints are executed sequentially

Example visualization:

Robot End Effector
        ↓
o----o----o----o
Trajectory Path
Troubleshooting
Controller not found

Check controllers:

ros2 control list_controllers

Expected controllers:

joint_state_broadcaster
xarm7_traj_controller
YAML file not found

Ensure the config file exists:

install/avatar_challenge/share/avatar_challenge/config/shapes.yaml

Rebuild if needed:

colcon build --symlink-install
Future Improvements

Potential extensions:

spline trajectory smoothing

dynamic shape switching

real-time drawing

trajectory preview

multi-shape drawing

Author

Wei Wang