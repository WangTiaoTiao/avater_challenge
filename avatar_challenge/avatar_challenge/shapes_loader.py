import rclpy
import numpy as np
import copy
from rclpy.node import Node
from tf_transformation import quaternion_from_euler, quaternion_matrix
import yaml
from pymoveit2 import MoveIt2

from geometry_msgs.msg import Pose

class ShapesLoader(Node):

    def __init__(self):

        super().__init__('shape_loader')

        self.movit2 = self.moveit2 = MoveIt2(
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

        self.poses = []

        self.load_shapes()

        self.plan_shapes()

    def load_shapes(self):

        with open('config/shapes.yaml') as f:
            data = yaml.safe_load(f)
        
        for s in data['shapes']:

            point_num = s['num']

            self.poses = [Pose() for _ in range(point_num+1)]

            # rotation
            q = quaternion_from_euler(
                s['start_pose']['rpy'][0],
                s['start_pose']['rpy'][1],
                s['start_pose']['rpy'][2]
            )
            t = quaternion_matrix(q)
            # translation
            t[0,3] = s['start_pose']['position'][0]
            t[1,3] = s['start_pose']['position'][1]
            t[2,3] = s['start_pose']['position'][2]

            for i in range(point_num + 1):
                
                msg = Pose()
                
                if i == 1 or i == point_num:
                    t_world = t
                else:
                    p = np.array([s['vertices'][i][0], s['vertices'][i][0], 0, 1.0])
                    t_world = t @ p
                
                msg.position.x =  t_world[0, 3]
                msg.position.y =  t_world[1, 3]
                msg.position.z =  t_world[2, 3]

                msg.orientaion.x = q[0]
                msg.orientaion.y = q[1]
                msg.orientaion.z = q[2]
                msg.orientaion.w = q[3]

                # self.publisher.publish(msg)
                self.poses[i] = msg

    def interpolation(self, p0, p1, steps = 50):

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
            pose.orientaion = p0.orientaion

            poses.append(pose)
        
        return poses

    def plan_shapes(self):

        self.waypoints = []

        for i in range(len(self.poses)-1):

            p0 = self.poses[i]
            p1 = self.poses[i+1]

            waypoints = self.interpolation(p0, p1)

            for p in waypoints:
                self.waypoints.append(copy.deepcopy(p))
        
        self.movit2.move_to_pose_sequence(self.waypoints)


def main():

    rclpy.init()

    node = ShapesLoader()

    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()


             
