import rclpy
import numpy as np
from rclpy.node import Node
from tf_transformation import quaternion_from_euler, quaternion_matrix

from geometry_msgs.msg import Pose

class ShapesPlanner(Node):

    def __init__(self):

        super().__init__('shape_planner')

        self.sub = self.create_subscription(Pose, '/TargetPose', self.targetpose_cb, 10)

        self.movit2 = Pose

    def targetpose_cb(self, msg):

