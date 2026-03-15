import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped


class DeadReckoningNode(Node):
    def __init__(self):
        super().__init__("dead_reckoning")

        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("ground_truth_topic", "/odom")
        self.declare_parameter("path_dr_topic", "/path_dr")
        self.declare_parameter("frame_id", "odom")
        self.declare_parameter("max_poses", 2000)

        cmd_topic = self.get_parameter("cmd_vel_topic").value
        gt_topic = self.get_parameter("ground_truth_topic").value
        path_topic = self.get_parameter("path_dr_topic").value
        self.frame_id = self.get_parameter("frame_id").value
        self.max_poses = int(self.get_parameter("max_poses").value)

        self.create_subscription(TwistStamped, cmd_topic, self.cmd_callback, 10)
        self.create_subscription(Odometry, gt_topic, self.gt_callback, 10)
        self.pub_path = self.create_publisher(Path, path_topic, 10)

        self.path_msg = Path()
        self.path_msg.header.frame_id = self.frame_id

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.last_time = None
        
        #прапорець для синхронізації
        self.initialized = False 
        
        self.gt_x = 0.0
        self.gt_y = 0.0

    def cmd_callback(self, msg: TwistStamped):
        # Чекаємо, поки не отримаємо координати для старту
        if not self.initialized:
            return 

        current_time = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        
        if self.last_time is None:
            self.last_time = current_time
            return
            
        dt = current_time - self.last_time
        self.last_time = current_time

        v = msg.twist.linear.x
        w = msg.twist.angular.z

        self.theta += w * dt
        self.x += v * math.cos(self.theta) * dt
        self.y += v * math.sin(self.theta) * dt

        pose = PoseStamped()
        pose.header.stamp = msg.header.stamp
        pose.header.frame_id = self.frame_id
        pose.pose.position.x = self.x
        pose.pose.position.y = self.y
        pose.pose.orientation.z = math.sin(self.theta / 2.0)
        pose.pose.orientation.w = math.cos(self.theta / 2.0)

        self.path_msg.poses.append(pose)
        if len(self.path_msg.poses) > self.max_poses:
            self.path_msg.poses = self.path_msg.poses[-self.max_poses:]
            
        self.pub_path.publish(self.path_msg)

    def gt_callback(self, msg: Odometry):
        self.gt_x = msg.pose.pose.position.x
        self.gt_y = msg.pose.pose.position.y

        #беремо реальні координати робота як стартову точку для математики!
        if not self.initialized:
            self.x = self.gt_x
            self.y = self.gt_y
            q = msg.pose.pose.orientation
            siny = 2.0 * (q.w * q.z + q.x * q.y)
            cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
            self.theta = math.atan2(siny, cosy)
            self.initialized = True
            self.get_logger().info("Синхронізовано стартову позицію!")
        
        error = math.sqrt((self.x - self.gt_x)**2 + (self.y - self.gt_y)**2)
        self.get_logger().info(f"Drift Error (Дрифт): {error:.3f} meters", throttle_duration_sec=2.0)


def main(args=None):
    rclpy.init(args=args)
    node = DeadReckoningNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()