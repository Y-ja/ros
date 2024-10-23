import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult

class SimpleParametor(Node):
    def __init__(self):
        super().__init__("simple_parametor")
        self.declare_parameter('🔧   Simple_parametor  🔧', '내가 만든 파라미터!')
        
        self.mypara = self.get_parameter('🔧   Simple_parametor  🔧').get_parameter_value().string_value
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.create_timer(1, self.print_hello)

    def print_hello(self):
        self.get_logger().info(f"parametor: {self.mypara}")

    def parameter_callback(self, params):
        for param in params:
            if param.name == '🔧   Simple_parametor  🔧':
                self.mypara = param.value
        return SetParametersResult(successful=True)  # 성공적인 결과 반환


def main():
    rclpy.init()
    node = SimpleParametor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Node has been stopped.")
        node.destroy_node()  # 강제 종료
    finally:
        rclpy.shutdown()  # ROS 2 종료

if __name__ == "__main__":
    main() 