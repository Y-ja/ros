import rclpy
from rclpy.node import Node


class SimpleParametor(Node):
    def __init__(self):
        super().__init__("simple_parametor")
        self.declare_parameter('🔧   Simple_parametor  🔧', '내가 만든 파라미터!')
        
        self.mypara = self.get_parameter('🔧   Simple_parametor  🔧').get_parameter_value().string_value
        self.create_timer(1, self.print_hello)

    def print_hello(self):
        self.get_logger().info(f"parametor: {self.mypara}")

def main():
    rclpy.init()
    node = SimpleParametor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__ == "__main__":
    main()
