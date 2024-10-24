import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import Parameter, ParameterType, ParameterValue
from rcl_interfaces.srv import SetParameters


class SimpleParametor2(Node):
    def __init__(self):
        super().__init__("simple_parametor")
        self.client = self.create_client(SetParameters, "/simple_parametor/set_parameters")
        
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Server is not available!")
        
        self.create_timer(1, self.print_parametor2)  # 메서드 이름 수정
        self.count = 0
        self.declare_parameter('number1' , 0)

    def print_parametor2(self):
        self.count += 1
        
        # Parameter 객체를 이름과 값으로 초기화
        param = Parameter(name='number_1', value=ParameterValue())
        param.value.type = ParameterType.PARAMETER_INTEGER
        param.value.integer_value = self.count
        
        req = SetParameters.Request()
        req.parameters = [param]
        
        # 요청을 보내고 응답을 기다림
        future = self.client.call_async(req)
        future.add_done_callback(self.done_callback)
    
    def done_callback(self, future):
        response = future.result()
        if response is not None:
            self.get_logger().info(f"Response: {response.results}")
        else:
            self.get_logger().error("Failed to get response.")


def main():
    rclpy.init()
    node = SimpleParametor2()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Node has been stopped.")
        node.destroy_node()  # 강제 종료
    finally:
        rclpy.shutdown()  # ROS 2 종료

if __name__ == "__main__":
    main()
