import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import qos_profile_sensor_data  # sensor_data QoS 프로파일 임포트

class Hello_pub(Node):
    def __init__(self):
        super().__init__("hello_pub")  # 부모 클래스(Node) 초기화
        
        # QoS 프로파일 설정
        self.qos_profile = qos_profile_sensor_data  # sensor_data QoS 프로파일 사용
        
        # 퍼블리셔 생성
        self.pub = self.create_publisher(String, "send", self.qos_profile)  
        
        self.create_timer(1, self.print_hello)  # 1초마다 print_hello 호출
        
        self.num = 0  # 메시지 카운트 초기화

    def sub_callback(self, msg):
        print(msg.data)  # 수신된 메시지 출력
        
    def print_hello(self):
        self.num += 1  # 메시지 카운트 증가
        msg = String()  # String 메시지 객체 생성
        msg.data = f"HELLO, ROS2_🐉_ {self.num}"  # 메시지 데이터 설정
        self.pub.publish(msg)  # 메시지 발행
        print("This is simlink really 🐉 !!")

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
