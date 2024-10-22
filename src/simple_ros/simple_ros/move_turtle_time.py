import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSDurabilityPolicy,
    QoSHistoryPolicy,
    QoSProfile,
    QoSReliabilityPolicy,
)
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from rclpy.duration import Duration  # Import Duration class

class MoveTurtle(Node):
    def __init__(self):
        super().__init__("move_turtle")
        
        self.qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_ALL,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.VOLATILE,
            depth=10
        )
        
        self.pub = self.create_publisher(Twist, "turtle1/cmd_vel", self.qos_profile)
        self.sub_pose = self.create_subscription(Pose, "turtle1/pose", self.pose_callback, self.qos_profile)

        self.twist = Twist()
        self.linear_velocity = 0.1  # Initial linear velocity
        self.angular_velocity = 0.5  # Constant angular velocity
        self.max_velocity = 1.0  # Maximum linear velocity
        self.duration = Duration(seconds=2)  # Duration for each movement phase
        self.start_time = self.get_clock().now()  # Record the start time
        self.moving_forward = True  # Flag for movement direction

        self.timer = self.create_timer(0.1, self.move_turtle)
        self.get_logger().info("Starting to move in a spiral pattern.")

    def move_turtle(self):
        current_time = self.get_clock().now()
        elapsed_time = current_time - self.start_time

        if self.moving_forward:
            # Gradually increase the linear velocity
            if self.linear_velocity < self.max_velocity:
                self.linear_velocity += 0.01  # Incremental increase

            # Set the twist velocities
            self.twist.linear.x = self.linear_velocity
            self.twist.angular.z = self.angular_velocity

            # Check if the movement duration has been reached
            if elapsed_time >= self.duration:
                self.moving_forward = False  # Change direction to turn
                self.start_time = current_time  # Reset start time
                self.get_logger().info("Reached maximum distance, turning.")

        else:
            # Reset velocity for turning
            self.twist.linear.x = 0.0
            self.twist.angular.z = self.angular_velocity

            # Check if the turning duration has been reached
            if elapsed_time >= self.duration:
                self.moving_forward = True  # Change direction to forward
                self.start_time = current_time  # Reset start time
                self.get_logger().info("Finished turning, moving forward.")

        # Publish the twist message
        self.pub.publish(self.twist)
        self.get_logger().info(f"Moving: linear.x={self.twist.linear.x}, angular.z={self.twist.angular.z}")

    def pose_callback(self, msg):
        self.get_logger().info(f"Received Pose: x={msg.x}, y={msg.y}, theta={msg.theta}")

def main():
    rclpy.init()
    node = MoveTurtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()
    finally:
        rclpy.shutdown()

if __name__ == "__main__":
    main()
