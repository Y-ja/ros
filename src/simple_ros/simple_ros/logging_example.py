import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from std_msgs.msg import String


class LoggerUsage(Node):
    def __init__(self):
        super().__init__("Logger_usage_demo")
        self.create_timer(1, self.on_timer)
        self.pub = self.create_publisher(String, "send", 10)
        self.number = 0

    def on_timer(self):
        self.get_logger().log(
            "timer_callback_called_(print once)",
             LoggingSeverity.INFO, 
             once=True)
        msg = String()
        msg.data = f"Current count: {self.number}"
        self.get_logger().info(f"Publishing: {msg.data}")
        self.pub.publish(msg)
        self.get_logger().info(msg.data)
        
        # Check if the count is a divisor of twelve
        if self.debug_function_to_evaluate():
            self.get_logger().debug("Count divides info 12")
        
        # Check if the count is even
        if self.number % 2 == 0:
            self.get_logger().debug("Count is even!")
        
        # Reset count if it exceeds 15
        if self.number > 15:
            self.get_logger().warn("Resetting count to 0!")
            self.number = 0
        
        # Increment the count
        self.number += 1
        
    def debug_function_to_evaluate(self):
        return is_divide_of_twelve(self.number, self.get_logger())
        
def is_divide_of_twelve(val, logger):
    if val == 0:
        logger.error("Module divisor cannot be 0")
        return False
    return (12 % val) == 0
    
def main():
    rclpy.init()
    node = LoggerUsage()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__ == "__main__":
    main()
