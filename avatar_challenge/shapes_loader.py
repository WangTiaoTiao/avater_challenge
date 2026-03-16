import rclpy
import numpy as np
import copy
import os
import time
import yaml

from rclpy.node import Node
from geometry_msgs.msg import Pose
from tf_transformations import quaternion_from_euler, quaternion_matrix
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from ament_index_python.packages import get_package_share_directory
from pymoveit2 import MoveIt2


class ShapesLoader(Node):

    def __init__(self):

        super().__init__('shape_loader')

        self.log("Shape Loader node started")

        self.traj_marker = []

        self.marker_pub = self.create_publisher(
            Marker,
            "trajectory_marker",
            10
        )

        # MoveIt2 interface
        self.moveit2 = MoveIt2(
            node=self,
            joint_names=[
                "joint1",
                "joint2",
                "joint3",
                "joint4",
                "joint5",
                "joint6",
                "joint7"
            ],
            base_link_name="link_base",
            end_effector_name="link_eef",
            group_name="xarm7"
        )

        self.log("Waiting for MoveIt2 system to be ready...")
        time.sleep(2)
        self.log("MoveIt2 ready")
        
        self.poses = []

        self.load_shapes()

        self.plan_shapes()

    def log(self, msg):
        """统一日志格式"""
        self.get_logger().info(f"[WW] {msg}")

    def publish_trajectory(self, pose):

        p = Point()
        p.x = pose.position.x
        p.y = pose.position.y
        p.z = pose.position.z

        self.traj_marker.append(p)

        marker = Marker()

        marker.header.frame_id = "link_base"
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = "trajectory"
        marker.id = 0

        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD

        marker.scale.x = 0.01

        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        marker.points = self.traj_marker

        self.marker_pub.publish(marker)

    def load_shapes(self):

        self.log("Loading shapes.yaml")

        package_path = get_package_share_directory('avatar_challenge')
        config_path = os.path.join(package_path, 'config', 'shapes.yaml')

        with open(config_path) as f:
            data = yaml.safe_load(f)

        for s in data['shapes']:

            point_num = s['num']

            self.log(f"Processing shape with {point_num} vertices")

            # 初始化 pose list
            poses_local = []

            # rotation
            q = quaternion_from_euler(
                s['start_pose']['rpy'][0],
                s['start_pose']['rpy'][1],
                s['start_pose']['rpy'][2]
            )

            # transformation matrix
            T = quaternion_matrix(q)

            # translation
            T[0, 3] = s['start_pose']['position'][0]
            T[1, 3] = s['start_pose']['position'][1]
            T[2, 3] = s['start_pose']['position'][2]

            for i in range(point_num + 1):

                msg = Pose()

                # 起点和终点
                if i == 0 or i == point_num:

                    msg.position.x = T[0, 3]
                    msg.position.y = T[1, 3]
                    msg.position.z = T[2, 3]

                else:

                    p = np.array([
                        s['vertices'][i][0],
                        s['vertices'][i][1],
                        0,
                        1.0
                    ])

                    p_world = T @ p

                    msg.position.x = p_world[0]
                    msg.position.y = p_world[1]
                    msg.position.z = p_world[2]

                msg.orientation.x = q[0]
                msg.orientation.y = q[1]
                msg.orientation.z = q[2]
                msg.orientation.w = q[3]

                poses_local.append(msg)

                self.log(
                    f"Pose {i}: "
                    f"x={msg.position.x:.3f}, "
                    f"y={msg.position.y:.3f}, "
                    f"z={msg.position.z:.3f}"
                )

            # 保存
            self.poses.extend(poses_local)

        self.log(f"Total poses loaded: {len(self.poses)}")

    def interpolation(self, p0, p1, steps=50):

        poses = []

        p0_vec = np.array([
            p0.position.x,
            p0.position.y,
            p0.position.z
        ])

        p1_vec = np.array([
            p1.position.x,
            p1.position.y,
            p1.position.z
        ])

        for t in np.linspace(0, 1, steps):

            pos = p0_vec * (1 - t) + p1_vec * t

            pose = Pose()

            pose.position.x = pos[0]
            pose.position.y = pos[1]
            pose.position.z = pos[2]

            pose.orientation = copy.deepcopy(p0.orientation)

            poses.append(pose)

        return poses

    def plan_shapes(self):

        self.log("Generating interpolated waypoints")

        waypoints = []

        for i in range(len(self.poses) - 1):

            p0 = self.poses[i]
            p1 = self.poses[i + 1]

            segment = self.interpolation(p0, p1)

            waypoints.extend(segment)

        for pose in waypoints:

            self.log(
                f"Moving to x={pose.position.x:.3f}, "
                f"y={pose.position.y:.3f}, "
                f"z={pose.position.z:.3f}"
            )

            self.moveit2.move_to_pose(
                position=[
                    pose.position.x,
                    pose.position.y,
                    pose.position.z
                ],
                quat_xyzw=[
                    pose.orientation.x,
                    pose.orientation.y,
                    pose.orientation.z,
                    pose.orientation.w
                ],
                cartesian=True
            )

            self.publish_trajectory(pose)
            
            self.moveit2.wait_until_executed()



def main():

    rclpy.init()

    node = ShapesLoader()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
