import rclpy
from rclpy.node import Node
from user_interface.msg import ArithmeticArgument
from user_interface.srv import ArithmeticOperator  # 서비스 임포트 수정

class Calculator(Node):
    def __init__(self):
        super().__init__("calculator")
        self.argument_a = 0.0
        self.argument_b = 0.0
        self.argument_formula = ''
        self.argument_result = 0.0
        self.argument_operator = '+'

        self.create_subscription(
            ArithmeticArgument,
            "arithmetic_argument",
            self.sub_callback,
            10
        )
        self.service_server = self.create_service(
            ArithmeticOperator,
            "arithmetic_operator",
            self.service_callback
        )

    def sub_callback(self, msg: ArithmeticArgument):
        self.argument_a = msg.argument_a
        self.argument_b = msg.argument_b
        self.get_logger().info(f"Time Stamp: {msg.stamp}")
        self.get_logger().info(f"Argument A: {self.argument_a}")
        self.get_logger().info(f"Argument B: {self.argument_b}")
        self.update_formula()

    def service_callback(self, request: ArithmeticOperator.Request, response: ArithmeticOperator.Response):
        if request.arithmetic_operator == ArithmeticOperator.Request.PLUS:
            self.argument_operator = '+'
        elif request.arithmetic_operator == ArithmeticOperator.Request.MINUS:
            self.argument_operator = '-'
        elif request.arithmetic_operator == ArithmeticOperator.Request.MULTIPLY:
            self.argument_operator = 'X'
        elif request.arithmetic_operator == ArithmeticOperator.Request.DIVISION:
            self.argument_operator = '/'
        
        self.update_formula()
        response.arithmetic_result = self.argument_result
        return response

    def update_formula(self):
        if self.argument_operator == '+':
            self.argument_result = self.argument_a + self.argument_b
        elif self.argument_operator == '-':
            self.argument_result = self.argument_a - self.argument_b
        elif self.argument_operator == 'X':
            self.argument_result = self.argument_a * self.argument_b
        elif self.argument_operator == '/':
            if self.argument_b != 0:
                self.argument_result = self.argument_a / self.argument_b
            else:
                self.get_logger().error("Division by zero error.")
                self.argument_result = 0.0  # ZeroDivisionError 처리
        self.argument_formula = f"{self.argument_result} = {self.argument_a} {self.argument_operator} {self.argument_b}"

def main():
    rclpy.init()
    node = Calculator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass  # 강제 종료 처리

    node.destroy_node()  # 노드 종료

if __name__ == "__main__":
    main()
