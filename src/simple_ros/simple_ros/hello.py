import rclpy
from rclpy.node import Node

def print_hello():
    
    print("HELLO, ROS2_🐉_")
    print("This is simlink really!!")


def main(): 
    rclpy.init()
    node = Node("hello")
     
    node.create_timer(1, print_hello)
    
    try:
        rclpy.spin(node)  # 노드가 계속 실행되도록 함
    except KeyboardInterrupt:
        print("Shutting down...")  # 종료 시 메시지 출력
    finally:
        node.destroy_node()  # 노드 삭제
        rclpy.shutdown()  # ROS 종료

if __name__ == "__main__":
    main()
