import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy

class Hello_sub(Node):
    def __init__(self):
        super().__init__("hello_sub")  # 부모 클래스(Node) 초기화
        
        # QoS 프로파일 설정
        self.qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_ALL,  # 모든 메시지 유지
            reliability=QoSReliabilityPolicy.RELIABLE,  # 신뢰성 있는 전송
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL  # 메시지의 지속성
        )
        
        # 퍼블리셔와 구독자 설정
        self.subscriber = self.create_subscription(
            String,           # 메시지 타입
            "send",           # 주제 이름
            self.sub_callback,  # 콜백 함수
            self.qos_profile   # QoS 프로파일 적용
        )

        self.create_timer(1, self.print_hello)  # 1초마다 print_hello 호출

    def sub_callback(self, msg):
        print(msg.data)  # 수신된 메시지 출력
        
    def print_hello(self):
        print("HELLO, ROS2_🐉_")
        print("This is simlink really!!")

def main(): 
    rclpy.init()
    node = Hello_sub()  # Hello_sub 인스턴스 생성
    
    try:
        rclpy.spin(node)  # 노드가 계속 실행되도록 함
    except KeyboardInterrupt:
        print("Shutting down...")  # 종료 시 메시지 출력
    finally:
        node.destroy_node()  # 노드 삭제
        if rclpy.ok():  # rclpy가 아직 종료되지 않은 경우
            rclpy.shutdown()  # ROS 종료

if __name__ == "__main__":
    main()
