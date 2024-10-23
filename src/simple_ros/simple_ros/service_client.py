import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSDurabilityPolicy,
    QoSHistoryPolicy,
    QoSProfile,
    QoSReliabilityPolicy,
)
from std_msgs.msg import String
from std_srvs.srv import SetBool

class ServiceClient(Node):
    def __init__(self):
        super().__init__("service_client")  # 노드 이름을 service_client로 변경
        # QoS 프로파일 설정
        self.qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_ALL,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        # 퍼블리셔 생성
        self.pub = self.create_publisher(String, "send", self.qos_profile)
        self.number = 0
        
        # 서비스 클라이언트 생성
        self.client = self.create_client(SetBool, "setBool")
        
        # 서비스가 사용 가능해질 때까지 대기
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available, waiting...")

        self.bool = False  # 초기값 설정
        
        # 타이머 설정 (3초마다 요청)
        self.create_timer(3.0, self.timer_callback)

    def timer_callback(self):
        # 예시로 True를 전달하여 요청
        self.send_request(True)

    def send_request(self, request_data):
        # 서비스 요청 생성
        request = SetBool.Request()
        request.data = request_data
        
        # 비동기 호출
        self.future = self.client.call_async(request)
        
        # 결과가 반환될 때까지 대기
        rclpy.spin_until_future_complete(self, self.future)
        
        # 결과 처리
        if self.future.result() is not None:
            self.get_logger().info(f"Service call successful: {self.future.result().message}")
        else:
            self.get_logger().error("Service call failed")

def main():
    rclpy.init()
    node = ServiceClient()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
