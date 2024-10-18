import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HelloNode(Node):
    def __init__(self):
        super().__init__("hello_class")  # 부모 클래스(Node) 초기화
        self.create_timer(1, self.print_hello)  # 1초마다 print_hello 호출
        self.pub = self.create_publisher(String, "send", 10)  # String 타입의 퍼블리셔 생성
        self.num = 0  # num 변수 초기화

    def print_hello(self):
        msg = String()  # String 메시지 객체 생성
        msg.data = "HELLO, ROS2_🐉_ " + str(self.num)  # 메시지 데이터 설정
        self.pub.publish(msg)  # 퍼블리셔를 사용하여 메시지 발행
        print("This is simlink really!!")
        self.num += 1  # num 증가

def main(): 
    rclpy.init()
    node = HelloNode()  # HelloNode 인스턴스 생성
    
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
