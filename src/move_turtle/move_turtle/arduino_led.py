import rclpy
import serial # type: ignore
from rclpy.node import Node
from std_msgs.msg import String


class Arduino_led(Node):
    def __init__(self):
        super().__init__("Arduino_led")
        # self.qos_profile = qos_profile_sensor_data
        self.create_subscription(String, "led", self.sub_callback, self.qos_profile)
        self.ser = serial.Serial('/dev.ttyUSB0' , 115200)

    def sub_callback(self, msg: String):
        
        byte_msg = msg.data.encode('utf-8')
        self.ser.write(byte_msg)
        self.get_logger().info(msg.data)

def main():
    rclpy.init()
    node = Arduino_led()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__ == "__main__":
    main()