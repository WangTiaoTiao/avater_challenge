
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
