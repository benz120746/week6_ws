#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import time
import math

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        
        self.publisher_ = self.create_publisher(TwistStamped, '/diff_drive_controller/cmd_vel', 10)
        self.get_logger().info('Publishing to /diff_drive_controller/cmd_vel')
        
        self.twist = TwistStamped()
        
    def move_forward(self, distance, speed=0.3):
        self.get_logger().info(f'⬆️  Moving forward {distance}m')
        duration = distance / speed
        self.twist.twist.linear.x = speed
        self.twist.twist.angular.z = 0.0
        
        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.twist.header.stamp = self.get_clock().now().to_msg()
            self.publisher_.publish(self.twist)
            time.sleep(0.1)
        self.stop()
        
    def move_backward(self, distance, speed=0.3):
        self.get_logger().info(f'⬇️  Moving backward {distance}m')
        duration = distance / speed
        self.twist.twist.linear.x = -speed
        self.twist.twist.angular.z = 0.0
        
        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.twist.header.stamp = self.get_clock().now().to_msg()
            self.publisher_.publish(self.twist)
            time.sleep(0.1)
        self.stop()
        
    def turn_left(self, angle=90, angular_speed=0.5):
        self.get_logger().info(f'⬅️  Turning left {angle}°')
        angle_rad = math.radians(angle)
        duration = angle_rad / angular_speed
        
        self.twist.twist.linear.x = 0.0
        self.twist.twist.angular.z = angular_speed
        
        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.twist.header.stamp = self.get_clock().now().to_msg()
            self.publisher_.publish(self.twist)
            time.sleep(0.1)
        self.stop()
        
    def turn_right(self, angle=90, angular_speed=0.5):
        self.get_logger().info(f'➡️  Turning right {angle}°')
        angle_rad = math.radians(angle)
        duration = angle_rad / angular_speed
        
        self.twist.twist.linear.x = 0.0
        self.twist.twist.angular.z = -angular_speed
        
        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.twist.header.stamp = self.get_clock().now().to_msg()
            self.publisher_.publish(self.twist)
            time.sleep(0.1)
        self.stop()
        
    def stop(self):
        self.twist.twist.linear.x = 0.0
        self.twist.twist.angular.z = 0.0
        self.twist.header.stamp = self.get_clock().now().to_msg()
        self.publisher_.publish(self.twist)
        time.sleep(0.5)

def main(args=None):
    rclpy.init(args=args)
    controller = RobotController()
    
    try:
        print("\n" + "="*60)
        print("       🤖 ROBOT MOVEMENT SEQUENCE 🤖")
        print("="*60 + "\n")
        
        # 1. เคลื่อนที่ไปข้างหน้า 1 เมตร
        print("Step 1: Moving forward 1 meter")
        controller.move_forward(distance=2.0, speed=0.3)
        time.sleep(1)
        
        # 2. เลี้ยวซ้าย 90°
        print("\nStep 2: Turning left 90°")
        controller.turn_left(angle=90, angular_speed=0.5)
        time.sleep(1)
        
        # 3. ถอยหลัง 1 เมตร
        print("\nStep 3: Moving backward 1 meter")
        controller.move_backward(distance=2.0, speed=0.3)
        time.sleep(1)
        
        # 4. เลี้ยวขวา 90°
        print("\nStep 4: Turning right 90°")
        controller.turn_right(angle=90, angular_speed=0.5)
        time.sleep(1)
        
        # 5. เคลื่อนที่ไปข้างหน้า 1 เมตร
        print("\nStep 5: Moving forward 1 meter")
        controller.move_forward(distance=2.0, speed=0.3)
        
        print("\n" + "="*60)
        print("       ✅ COMPLETED! ✅")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\nStopping...")
        controller.stop()
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
