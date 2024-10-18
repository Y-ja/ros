import rclpy
from rclpy.clock import Clock, ClockType
from rclpy.node import Node
from rclpy.qos import (
    QoSDurabilityPolicy,
    QoSHistoryPolicy,
    QoSProfile,
    QoSReliabilityPolicy,
)
from std_msgs.msg import Header

class TimePub(Node):
    def __init__(self):
        super().__init__("time_pub")
        
        # QoS 프로필 정의
        self.qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            durability=QoSDurabilityPolicy.VOLATILE,
            depth=10
        )
        
        # 매초 print_hello를 호출하는 타이머 생성
        self.create_timer(1.0, self.print_hello)
        
        # 'time' 토픽에 대한 퍼블리셔 생성
        self.pub = self.create_publisher(Header, "time", self.qos_profile)
        
        # ROS 시간 사용
        self.clock = Clock(clock_type=ClockType.ROS_TIME)

    def print_hello(self):
        # Header 메시지 생성
        msg = Header()
        msg.frame_id = "time"
        msg.stamp = self.clock.now().to_msg()
        
        # 시간을 로그로 출력
        self.get_logger().info(f"sec: {msg.stamp.sec}, nano sec: {msg.stamp.nanosec}")
        
        # 메시지 퍼블리시
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = TimePub()
    try:
        rclpy.spin(node)  # 노드가 계속 실행되도록 함
    except KeyboardInterrupt:
        print("Shutting down...")  # 종료 시 메시지 출력
    finally:
        node.destroy_node()  # 노드 삭제
        if rclpy.ok():  # rclpy가 정상적으로 작동 중인 경우
            rclpy.shutdown()  # ROS 종료

if __name__ == "__main__":
    main()
