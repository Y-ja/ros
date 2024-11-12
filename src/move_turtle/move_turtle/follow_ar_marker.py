import math
import rclpy
from rclpy.node import Node  # Node 클래스 임포트
from rclpy.qos import qos_profile_sensor_data  # qos_profile_sensor_data 임포트
from geometry_msgs.msg import Pose, Twist
from ros2_aruco_interfaces.msg import ArucoMarkers
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion

MAX_VEL = 0.21
MAX_ANGLE = 2.8  # radian/sec

class Move_turtle(Node):
    def __init__(self):
        super().__init__("follow_ar_marker")
        self.qos_profile = qos_profile_sensor_data  # QoS 프로파일 설정
        self.create_timer(0.1, self.twist_pub)
        self.create_timer(1/60, self.update)
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.create_subscription(LaserScan, "/scan", self.laser_callback, self.qos_profile)
        self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
        self.create_subscription(ArucoMarkers, "/aruco_markers", self.aruco_callback, 10)
        
        self.twist = Twist()
        self.odom = Odometry()
        self.aruco_markers = ArucoMarkers()
        self.follow_tf = Pose()
        self.theta = 0.0  # robot's current orientation (in radians)
        self.target_marker = None  # Store the marker we are following

    def twist_pub(self):
        self.restrain()
        self.pub.publish(self.twist)

    def aruco_callback(self, msg: ArucoMarkers):
        """ Aruco marker가 감지되면 follow_tf를 업데이트하고, 마커를 추적하도록 명령 """
        self.aruco_markers = msg
        for marker_id_ele in msg.marker_ids:
            if marker_id_ele == 1:  # 마커 ID가 1인 경우에만 추적
                self.target_marker = msg.poses[msg.marker_ids.index(marker_id_ele)]
                self.follow_tf = self.target_marker
                break  # 첫 번째로 감지된 마커만 추적

    def odom_callback(self, msg: Odometry):
        """ Odometry를 통해 로봇의 현재 방향을 업데이트 """
        self.odom = msg
        x = msg.pose.pose.orientation.x
        y = msg.pose.pose.orientation.y
        z = msg.pose.pose.orientation.z
        w = msg.pose.pose.orientation.w
        _, _, self.theta = euler_from_quaternion((x, y, z, w))

    def update(self):
        """ 로봇이 마커를 향해 움직이도록 속도 명령을 생성 """
        if self.target_marker:
            # 마커의 상대 위치 계산
            marker_x = self.follow_tf.position.x
            marker_y = self.follow_tf.position.y

            # 로봇의 현재 위치와 마커의 위치 차이 계산
            dx = marker_x - self.odom.pose.pose.position.x
            dy = marker_y - self.odom.pose.pose.position.y

            # 로봇이 마커를 향해 회전할 각도 계산
            angle_to_marker = math.atan2(dy, dx)
            angle_diff = angle_to_marker - self.theta

            # 각도 차이를 -π에서 π 범위로 조정
            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            elif angle_diff < -math.pi:
                angle_diff += 2 * math.pi

            # 로봇의 속도 계산
            self.twist.angular.z = 1.5 * angle_diff  # 각도 비례 제어
            self.twist.linear.x = 0.5 * math.sqrt(dx**2 + dy**2)  # 직선 거리 비례 제어

            # 마커가 충분히 가까워지면 멈추기
            if abs(dx) < 0.1 and abs(dy) < 0.1:
                self.twist.linear.x = 0
                self.twist.angular.z = 0
        else:
            # 마커가 없을 경우, 멈춤
            self.twist.linear.x = 0
            self.twist.angular.z = 0

    def restrain(self):
        """ 속도 제한 """
        self.twist.linear.x = min(self.twist.linear.x, MAX_VEL)
        self.twist.linear.x = max(self.twist.linear.x, -MAX_VEL)
        self.twist.angular.z = min(self.twist.angular.z, MAX_ANGLE)
        self.twist.angular.z = max(self.twist.angular.z, -MAX_ANGLE)

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
