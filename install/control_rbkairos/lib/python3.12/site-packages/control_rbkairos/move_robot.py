import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class MoveRobot(Node):
    def __init__(self):
        super().__init__('move_robot')
        self.pub = self.create_publisher(Twist, 'robot1/cmd_vel', 10)
        self.get_logger().info('Publishing to robot1/cmd_vel')

    def move_square(self, v=0.2, w=0.6, straight_time=2.0, turn_time=1.7, repeat=2):
        twist = Twist()
        for i in range(repeat):
            self.get_logger().info(f'Go straight #{i+1}')
            t0 = time.time()
            while time.time() - t0 < straight_time:
                twist.linear.x = v
                twist.angular.z = 0.0
                self.pub.publish(twist)
                rclpy.spin_once(self, timeout_sec=0.01)

            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.pub.publish(twist)
            time.sleep(0.2)

            self.get_logger().info(f'Turn #{i+1}')
            t0 = time.time()
            while time.time() - t0 < turn_time:
                twist.linear.x = 0.0
                twist.angular.z = w
                self.pub.publish(twist)
                rclpy.spin_once(self, timeout_sec=0.01)

        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.pub.publish(twist)
        self.get_logger().info('Done!')

def main():
    rclpy.init()
    node = MoveRobot()
    try:
        node.move_square()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
