import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Hello(Node):
    def __init__(self):
        super().__init__("hello")
        self.create_timer(1, self.print_hello)
        self.pub = self.create_publisher(String, "send", 10)
        self.number = 0

    def print_hello(self):
        msg = String()
        msg.data = f"HELLO, ROS2_🐉_ {self.number}"  # 메시지 데이터 설정
        self.pub.publish(msg)
        print("hello, ros2! nice to meet you!")
        self.number += 1

def main(): 
    rclpy.init()
    node = Hello()  # Hello 인스턴스 생성
    
    try:
        rclpy.spin(node)  # 노드가 계속 실행되도록 함
    except KeyboardInterrupt:
        print("Shutting down...")  # 종료 시 메시지 출력
    finally:
        if rclpy.ok():  # rclpy가 정상적으로 작동 중인 경우
            node.destroy_node()  # 노드 삭제
            rclpy.shutdown()  # ROS 종료

if __name__ == "__main__":
    main()
