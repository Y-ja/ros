import rclpy
import time
from rclpy.node import Node
from rclpy.qos import (
    QoSDurabilityPolicy,
    QoSHistoryPolicy,
    QoSProfile,
    QoSReliabilityPolicy,
)
from std_msgs.msg import String
from std_srvs.srv import SetBool

class ServiceServer(Node):
    def __init__(self):
        super().__init__("ServiceServer")
        # QoS 프로파일 설정
        self.qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_ALL,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        # 서비스 생성
        self.create_service(SetBool, "setBool", self.set_bool_callback)
        # 퍼블리셔 생성
        self.pub = self.create_publisher(String, "send", self.qos_profile)
        self.number = 0
        self.bool = False  # 초기값 설정

    def set_bool_callback(self, request, response: SetBool.Response):
        # 요청 데이터가 True일 때만 메시지를 게시
        if request.data:  
            msg = String()
            msg.data = f"hello, ros2! nice to meet you! + {self.number}"
            self.pub.publish(msg)
            self.get_logger().info(msg.data)
            self.number += 1
            response.success = True
            response.message = "Message published."
            time.sleep(1)  # 메시지 전송 후 1초 대기
        else:
            response.success = False
            response.message = "Message not published due to false request."
        return response

def main():
    rclpy.init()
    node = ServiceServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
