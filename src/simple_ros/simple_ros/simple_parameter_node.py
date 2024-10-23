import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult

class SimpleParametor(Node):
    def __init__(self):
        super().__init__("simple_parametor")
        
        # 파라미터 선언
        self.declare_parameter("parametor", "내가 만든 파라미터!")
        self.declare_parameter("node_name", "내가 만든 노드 이름!")
        self.declare_parameter("number1", 123456)
        self.declare_parameter("number2", 3.141592)

        # 초기 파라미터 값 가져오기
        self.mypara = self.get_parameter("parametor").get_parameter_value().string_value
        self.node_name = self.get_parameter("node_name").get_parameter_value().string_value
        self.number1 = self.get_parameter("number1").get_parameter_value().integer_value
        self.number2 = self.get_parameter("number2").get_parameter_value().double_value

        # 파라미터 콜백 추가
        self.add_on_set_parameters_callback(self.parameter_callback)

        # 타이머 생성
        self.create_timer(1, self.print_parameters)

    def print_parameters(self):
        self.get_logger().info(f"parametor: {self.mypara}")
        self.get_logger().info(f"node_name: {self.node_name}")
        self.get_logger().info(f"number1: {self.number1}")
        self.get_logger().info(f"number2: {self.number2:.6f}")

    def parameter_callback(self, params):
        for param in params:
            if param.name == "parametor":
                self.mypara = param.value
            elif param.name == "node_name":
                self.node_name = param.value
            elif param.name == "number1":
                self.number1 = param.value
            elif param.name == "number2":
                self.number2 = param.value
        return SetParametersResult(successful=True)

def main():
    rclpy.init()
    node = SimpleParametor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Node has been stopped.")
        node.destroy_node()
    finally:
        rclpy.shutdown()

if __name__ == "__main__":
    main()
