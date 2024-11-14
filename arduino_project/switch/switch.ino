const int buttonPin = 2;  // 버튼 핀 번호
int buttonState = 0;       // 버튼 상태 저장 변수
int lastButtonState = HIGH; // 이전 버튼 상태 (초기값: 버튼이 떼어져 있는 상태)
bool flag = 0;             // 버튼이 눌린 상태를 추적하는 플래그
unsigned long prev_time = 0;  // 시간 추적 변수

void setup() {
    Serial.begin(115200);        // 시리얼 통신 시작
    pinMode(buttonPin, INPUT_PULLUP);  // 버튼 핀을 풀업 입력 모드로 설정
}

void loop() {
    buttonState = digitalRead(buttonPin);  // 버튼 상태 읽기
    
    // 버튼이 눌린 상태에서 변화를 감지
    if (buttonState == LOW && lastButtonState == HIGH) {
        // 버튼이 눌리기 시작한 경우 (전환 상태)
        prev_time = millis();  // 시간 기록
        Serial.println("Button Pressed!");
    } 
    
    // 버튼이 떼어진 상태에서 변화를 감지
    else if (buttonState == HIGH && lastButtonState == LOW) {
        // 버튼이 떼어진 경우 (전환 상태)
        Serial.println("Button Released!");
    }
    
    // 마지막 버튼 상태 업데이트
    lastButtonState = buttonState;

    delay(100);  // 버튼 상태 체크 주기 100ms
}
