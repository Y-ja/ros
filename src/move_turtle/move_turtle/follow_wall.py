import math

import rclpy
import tf2_ros
from geometry_msgs.msg import TransformStamped, Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import BatteryState, Imu, LaserScan
from tf2_ros import Buffer, TransformBroadcaster, TransformListener

MAX_VEL = 0.21
MAX_ANGLE = 2.8 # radian/sec

def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z # in radians

class Move_turtle(Node):
    def __init__(self):
        super().__init__("hello_pub")
        self.qos_profile = qos_profile_sensor_data
        self.create_timer(0.1, self.twist_pub)
        self.create_timer(1/60, self.update)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.create_subscription(LaserScan, "/scan", self.laser_callback, self.qos_profile)
        self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
        self.create_subscription(Imu, "/imu", self.imu_callback, 10)
        self.create_subscription(BatteryState, "/battery_state", self.battery_callback, 10)
        self.twist = Twist()
        self.laserscan = LaserScan()
        self.odom = Odometry()
        self.imu = Imu()
        self.battery = BatteryState()
        self.theta = 0.0 # radians
        self.phase = 0
        self.laserscan_degree = [3.5 for i in range(360)]
        self.find_wall = False
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # Create a tf2 Buffer and TransformListener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def twist_pub(self):
        self.restrain()
        self.pub.publish(self.twist)

    def laser_callback(self, msg: LaserScan):
        self.laserscan = msg
        count = 0
        self.get_logger().info(f"self.laserscan_degree -> {self.laserscan_degree}")
        for s_radian in self.laserscan.ranges:
            radian_index = msg.angle_min + msg.angle_increment * count
            degree_index = int(radian_index / 3.141592 * 180)
            if s_radian == float('inf'):
                s_radian = msg.range_max
            self.laserscan_degree[degree_index] = s_radian
            count += 1
        self.wall_45_collision_point_function()

    def wall_45_collision_point_function(self):
        # turtlebot current position
        x = self.odom.pose.pose.position.x
        y = self.odom.pose.pose.position.y
        theta = self.theta
        # 45 degree laser distance
        laser_45 = self.laserscan_degree[45]
        # 90 degree laser distance
        laser_90 = self.laserscan_degree[90]
        # Wall collision point at 45 degree
        wall_45_collision_point = (
            x + laser_45 * math.cos(theta + math.pi / 4),
            y + laser_45 * math.sin(theta + math.pi / 4))
        # Wall collision point at 90 degree
        wall_90_collision_point = (
            x + laser_90 * math.cos(theta + math.pi / 2),
            y + laser_90 * math.sin(theta + math.pi / 2))
        # Slope between the two collision points
        slope = math.atan2(wall_45_collision_point[1] - wall_90_collision_point[1], wall_45_collision_point[0] - wall_90_collision_point[0])
        # Perpendicular slope
        slope_90 = slope - math.pi / 2
        # 0.4m offset point from the 45-degree collision point in the perpendicular direction
        wall_45_collision_point_0_4 = (
            wall_45_collision_point[0] + 0.4 * math.cos(slope_90),
            wall_45_collision_point[1] + 0.4 * math.sin(slope_90))
        # Send the transform to follow_point
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "odom"
        t.child_frame_id = "follow_point"
        t.transform.translation.x = wall_45_collision_point_0_4[0]
        t.transform.translation.y = wall_45_collision_point_0_4[1]
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
        self.tf_broadcaster.sendTransform(t)

    def odom_callback(self, msg: Odometry):
        self.odom = msg
        x = msg.pose.pose.orientation.x
        y = msg.pose.pose.orientation.y
        z = msg.pose.pose.orientation.z
        w = msg.pose.pose.orientation.w
        _, _, self.theta = euler_from_quaternion(x, y, z, w)

    def imu_callback(self, msg: Imu):
        self.imu = msg

    def battery_callback(self, msg: BatteryState):
        self.battery = msg

    def update(self):
        buffer = self.tf_buffer
        try:
            if not self.find_wall:
                self.twist.linear.x = MAX_VEL / 2
                self.twist.angular.z = 0.0
                if self.laserscan_degree[0] < 0.4:
                    self.find_wall = True
            else:
                # Look up the transform from base_footprint to follow_point
                follow_tf = buffer.lookup_transform("base_footprint", "follow_point", rclpy.time.Time())
                # Compute angular velocity based on the transform
                self.twist.angular.z = math.atan2(follow_tf.transform.translation.y, follow_tf.transform.translation.x)
                # Compute linear velocity based on the distance to follow_point
                self.twist.linear.x = math.sqrt(follow_tf.transform.translation.x**2 + follow_tf.transform.translation.y**2)
        except tf2_ros.LookupException as e:
            self.get_logger().warn(f"Transform lookup failed: {e}")
            if not self.find_wall:
                self.twist.linear.x = MAX_VEL / 2
                self.twist.angular.z = 0.0
                if self.laserscan_degree[0] < 0.4:
                    self.find_wall = True
            else:
                # Corner case logic
                if self.laserscan_degree[45] > 1.00:
                    self.twist.linear.x = MAX_VEL / 4
                    self.twist.angular.z = MAX_ANGLE / 8
                elif self.laserscan_degree[45] + self.laserscan_degree[135] > 1.00:
                    self.twist.linear.x = MAX_VEL / 4
                    if self.laserscan_degree[45] > self.laserscan_degree[135]:
                        self.twist.angular.z = MAX_ANGLE / 8
                    else:
                        self.twist.angular.z = -MAX_ANGLE / 8
                elif self.laserscan_degree[45] + self.laserscan_degree[135] < 0.8:
                    self.twist.linear.x = MAX_VEL / 4
                    self.twist.angular.z = -MAX_ANGLE / 8
                else:
                    if self.laserscan_degree[45] > self.laserscan_degree[135]:
                        self.twist.linear.x = MAX_VEL / 2
                        self.twist.angular.z = MAX_ANGLE / 8
                    else:
                        self.twist.linear.x = MAX_VEL / 2
                        self.twist.angular.z = -MAX_ANGLE / 8

    def restrain(self):
        self.twist.linear.x = min([self.twist.linear.x, MAX_VEL])
        self.twist.linear.x = max([self.twist.linear.x, -MAX_VEL])
        self.twist.angular.z = min([self.twist.angular.z, MAX_ANGLE])
        self.twist.angular.z = max([self.twist.angular.z, -MAX_ANGLE])

def main():
    rclpy.init()
    node = Move_turtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        for _ in range(10):
            node.pub.publish(Twist())
        node.destroy_node()

if __name__ == "__main__":
    main()
