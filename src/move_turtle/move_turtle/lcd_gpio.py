import time
import rclpy
from move_turtle import RPi_I2C_driver
from rclpy.node import Node
from tb_interface.srv import LcdDisplay

class LcdServer(Node):
    def __init__(self):
        super().__init__("lcd_server")
        self.create_service(LcdDisplay, "lcd_server", self.set_display_callback)
        # lcd 초기화
        self.lcd = RPi_I2C_driver.lcd(0x27)  # I2C 주소 0x27 설정
        self.lcd.cursor()  # 커서 활성화

    def set_display_callback(self, request: LcdDisplay.Request, response: LcdDisplay.Response):
        # 요청된 데이터 출력
        self.get_logger().info(f"Request received: {request.data}")
        
        # 요청 데이터를 문자열로 변환
        lcd_input = f"{request.data}"

        # 'lcd'로 시작하는 데이터 처리
        if lcd_input[0:3] == "lcd":
            # 커서 위치 설정
            if lcd_input[3] == "0":
                self.lcd.setCursor(0, 0)
            elif lcd_input[3] == "1":
                self.lcd.setCursor(0, 1)
            elif lcd_input[3] == "2":
                self.lcd.setCursor(0, 2)
            elif lcd_input[3] == "3":
                self.lcd.setCursor(0, 3)
            else:
                self.get_logger().warn("Invalid line number received, valid values are 0, 1, 2, 3.")
                response.success = False
                return response

            # lcd에 데이터 표시
            self.lcd.print(f"{lcd_input[4:]}")
            self.get_logger().info(f"Data displayed on LCD: {lcd_input[4:]}")
        
        # 응답 성공 여부 설정
        response.success = True
        return response

def main():
    rclpy.init()
    node = LcdServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()

if __name__ == "__main__":
    main()
