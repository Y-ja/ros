import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSDurabilityPolicy,
    QoSHistoryPolicy,
    QoSProfile,
    QoSReliabilityPolicy,
)
from std_msgs.msg import String

class Hello_pub(Node):
    def __init__(self):
        super().__init__("hello_pub")
        
        # QoS 프로파일 설정
        self.qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_ALL,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        
        self.create_timer(1, self.print_hello)  # 1초마다 print_hello 호출
        self.pub = self.create_publisher(String, "send", self.qos_profile)  # 퍼블리셔 생성
        
        self.number = 0  # 메시지 카운트 초기화

    def print_hello(self):
        msg = String()  # String 메시지 객체 생성
        msg.data = f"hello, ros2! nice to meet you! + {self.number}"  # 메시지 데이터 설정
        self.pub.publish(msg)  # 메시지 발행
        print(msg.data)  # 발행된 메시지 출력
        self.number += 1  # 메시지 카운트 증가

def main():
    rclpy.init()
    node = Hello_pub()  # Hello_pub 인스턴스 생성
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
