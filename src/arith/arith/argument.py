import rclpy
import random
from rclpy.node import Node
from user_interface.msg import ArithmeticArgument  # 메시지 임포트

class Argument(Node):
    def __init__(self):
        super().__init__("argument")
        self.declare_parameter("min", 0)
        self.declare_parameter("max", 30)
        
        self.min = self.get_parameter("min").get_parameter_value().integer_value
        self.max = self.get_parameter("max").get_parameter_value().integer_value
        
        self.add_on_set_parameters_callback(self.update_parameter)
        
        self.create_timer(1.0, self.pub)
        self.pub_o = self.create_publisher(ArithmeticArgument, "arithmetic_argument", 10)
        
    def update_parameter(self, params):
        for param in params:
            if param.name == "min":
                self.min = param.value
            elif param.name == "max":
                self.max = param.value
        return rclpy.parameter.SetParametersResult(successful=True)

    def pub(self):
        msg = ArithmeticArgument()
        msg.stamp = self.get_clock().now().to_msg()
        msg.argument_a = float(random.randint(self.min, self.max))
        msg.argument_b = float(random.randint(self.min, self.max))
        self.get_logger().warn(f"Argument A -> {msg.argument_a}")
        self.get_logger().warn(f"Argument B -> {msg.argument_b}")
        self.pub_o.publish(msg)
            
def main():
    rclpy.init()
    node = Argument()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass  # 강제 종료 처리

    node.destroy_node()  # 노드 종료

if __name__ == "__main__":
    main()
