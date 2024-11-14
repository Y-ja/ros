#include <Arduino.h>
#include <Servo.h>

Servo servo;
int angle = 0;
int SERVO_PIN = 6;

void setup()
{
    servo.attach(SERVO_PIN);  // 서보 모터를 연결
    Serial.begin(9600);  // 시리얼 통신을 9600 baud rate로 시작
}

void loop()
{
    static String buffer;

    // 시리얼로 데이터가 들어오면
    if (Serial.available() > 0)
    {
        buffer = Serial.readStringUntil('\n');  // 한 줄 읽기
        
        // "move" 명령어가 오면
        if (buffer.substring(0, 4) == "move")
        {
            // "move" 뒤에 오는 두 숫자(서보의 각도)를 읽어서 pos로 변환
            int pos = buffer.substring(4, 6).toInt();  // 두 번째에서 여섯 번째까지의 값을 정수로 변환
            servo.write(pos);  // 해당 각도로 서보 모터를 이동
        }
    }

    // 서보 모터를 0도에서 180도까지 이동
    for (angle = 0; angle <= 180; angle++)  
    {
        servo.write(angle);  // 서보에 angle 값을 전달
        delay(15);  // 서보가 이동할 시간을 주기 위해 잠시 대기
    }

    // 서보 모터를 180도에서 0도로 돌아가게 이동
    for (angle = 180; angle >= 0; angle--)  
    {
        servo.write(angle);  // 서보에 angle 값을 전달
        delay(15);  // 서보가 이동할 시간을 주기 위해 잠시 대기
    }
}
