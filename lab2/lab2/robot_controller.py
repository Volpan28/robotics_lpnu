#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.counter = 0
        self.get_logger().info('Robot Controller started - publishing to /cmd_vel')

    def timer_callback(self):
        """Called every 0.1 seconds to publish velocity commands"""
        msg = Twist()
        
        # Example: Move forward with sinusoidal turning
        msg.linear.x = 0.5  # 0.5 m/s forward
        msg.angular.z = 0.3 * math.sin(self.counter * 0.1)  # Wavy motion
        
        self.publisher.publish(msg)
        self.counter += 1
        
        # Log every 5 seconds
        if self.counter % 50 == 0:
            self.get_logger().info(
                f'Publishing: linear.x={msg.linear.x:.2f}, '
                f'angular.z={msg.angular.z:.2f}'
            )

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    
    try:
        rclpy.spin(node)  # Keep node running
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()