import math
import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import BatteryState, Imu, LaserScan

MAX_VEL = 0.21
MAX_ANGLE = 2.8  # radian/sec

def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into Euler angles (roll, pitch, yaw)
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

    return roll_x, pitch_y, yaw_z  # in radians

class MoveTurtle(Node):
    def __init__(self):
        super().__init__("hello_pub")
        self.qos_profile = qos_profile_sensor_data
        self.create_timer(0.1, self.twist_pub)  # Timer for publishing twist
        self.create_timer(1 / 60, self.update)  # Timer for update logic (lower rate)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.create_subscription(LaserScan, "/scan", self.laser_callback, self.qos_profile)
        self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
        self.create_subscription(Imu, "/imu", self.imu_callback, 10)
        self.create_subscription(BatteryState, "/battery_state", self.battery_callback, 10)

        # Initialize attributes
        self.twist = Twist()
        self.laserscan = LaserScan()
        self.odom = Odometry()
        self.imu = Imu()
        self.battery = BatteryState()
        self.theta = 0.0  # Radian (yaw)
        self.phase = 0
        self.laserscan_degree = [3.5 for _ in range(360)]  # Array for storing laser data in degrees

    def twist_pub(self):
        self.restrain()  # Make sure the twist is within limits
        self.pub.publish(self.twist)

    def laser_callback(self, msg: LaserScan):
        """ Callback for laser scan data """
        self.laserscan = msg
        count = 0
        for s_radian in self.laserscan.ranges:
            radian_index = msg.angle_min + msg.angle_increment * count
            degree_index = int(radian_index / math.pi * 180)  # Convert radians to degrees
            if s_radian == float('inf'):
                s_radian = msg.range_max  # Replace 'inf' values with the max range
            # Ensure the index is within bounds (0-359 degrees)
            if 0 <= degree_index < 360:
                self.laserscan_degree[degree_index] = s_radian
            count += 1

    def odom_callback(self, msg: Odometry):
        """ Callback for odometry data """
        self.odom = msg
        x = msg.pose.pose.orientation.x
        y = msg.pose.pose.orientation.y
        z = msg.pose.pose.orientation.z
        w = msg.pose.pose.orientation.w
        _, _, self.theta = euler_from_quaternion(x, y, z, w)

    def imu_callback(self, msg: Imu):
        """ Callback for IMU data (currently unused) """
        self.imu = msg
        # You can extract more IMU data if necessary

    def battery_callback(self, msg: BatteryState):
        """ Callback for battery data (currently unused) """
        self.battery = msg
        # You can extract more battery data if necessary

    def update(self):
        """ Logic for controlling the robot's movement using sensor data """
        # Example logic: Move forward if nothing is in front, rotate if obstacle is detected
        # We use the laser scan data to check for obstacles
        front_distance = self.laserscan_degree[0]  # Get distance at 0 degrees (directly ahead)
        
        if front_distance < 1.0:  # If there's an obstacle within 1 meter
            self.twist.linear.x = 0.0  # Stop moving forward
            self.twist.angular.z = 0.5  # Rotate
        else:
            self.twist.linear.x = 0.1  # Move forward slowly
            self.twist.angular.z = 0.0  # No rotation

    def restrain(self):
        """ Ensure that velocities do not exceed max limits """
        self.twist.linear.x = min([self.twist.linear.x, MAX_VEL])
        self.twist.linear.x = max([self.twist.linear.x, -MAX_VEL])
        self.twist.angular.z = min([self.twist.angular.z, MAX_ANGLE])
        self.twist.angular.z = max([self.twist.angular.z, -MAX_ANGLE])

def main():
    rclpy.init()
    node = MoveTurtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Stop the robot before shutting down
        for _ in range(10):
            node.pub.publish(Twist())  # Stop movement by publishing zero velocities
        node.destroy_node()

if __name__ == "__main__":
    main()
