"""Figure-8 path - STUDENT TASK.
Implement a figure-8: two circles, first turning left, then turning right.
"""
import time
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

from .diff_drive_math import twist_to_wheel_speeds


class Figure8Path(Node):
    def __init__(self):
        super().__init__('figure_8_path')

        self.declare_parameter("linear_speed", 0.3)
        self.declare_parameter("angular_speed", 0.4)
        self.declare_parameter("rate_hz", 20.0)

        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        self.get_logger().info("Starting figure-8 path")

        v = float(self.get_parameter("linear_speed").value)
        w = float(self.get_parameter("angular_speed").value)
        
        # Виконуємо перше коло (вліво, w > 0)
        self.get_logger().info("Circle 1: turning left")
        self.run_circle(v, w)
        
        # Виконуємо друге коло (вправо, w < 0)
        self.get_logger().info("Circle 2: turning right")
        self.run_circle(v, -w)

        self.get_logger().info("Figure-8 complete.")

    def run_circle(self, v, w):
        dt = 1.0 / max(float(self.get_parameter("rate_hz").value), 1.0)
        duration = (2.0 * math.pi / max(abs(w), 1e-6)) * 1.60
        
        msg = TwistStamped()
        msg.header.frame_id = 'base_link'
        msg.twist.linear.x = v
        msg.twist.angular.z = w

        t_end = time.time() + duration
        while time.time() < t_end:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(dt)

        stop_msg = TwistStamped()
        self.pub.publish(stop_msg)
        time.sleep(0.5)


def main(args=None):
    rclpy.init(args=args)
    node = Figure8Path()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()