#include <Arduino.h>
#include <string.h>  // C 스타일 문자열을 위한 라이브러리

class Switch
{
public:
    Switch(int buttonPin, bool pullup = true)
        : _buttonPin(buttonPin), _prev_time(millis()), _buttonState(HIGH), _flag(false)
    {
        if (pullup)
        {
            pinMode(_buttonPin, INPUT_PULLUP);
        }
        else
        {
            pinMode(_buttonPin, INPUT);
        }
    }

    // 버튼 상태를 반환하는 함수
    const char* read()
    {
        _buttonState = digitalRead(_buttonPin);  // 버튼 상태 읽기

        // 버튼이 눌리면
        if (_buttonState == LOW)
        {
            // 버튼이 처음 눌린 경우에만 출력
            if (!_flag && (millis() - _prev_time) > 100)  // 디바운싱
            {
                _prev_time = millis();  // 시간 갱신
                _flag = true;  // 버튼이 눌렸다고 플래그 설정
                snprintf(_buttonMessage, sizeof(_buttonMessage), "button_on_%d", _buttonPin);
                return _buttonMessage;  // 버튼이 눌렸을 때 메시지 반환
            }
        }
        // 버튼이 떼어졌을 때
        else if (_flag)
        {
            _flag = false;  // 버튼이 떼어진 상태로 설정
            _prev_time = millis();  // 시간 갱신
            snprintf(_buttonMessage, sizeof(_buttonMessage), "button_off_%d", _buttonPin);
            return _buttonMessage;  // 버튼이 떼어졌을 때 메시지 반환
        }

        return nullptr;  // 상태 변화가 없을 때는 NULL 반환
    }

private:
    int _buttonPin;          // 버튼 핀
    int _buttonState;        // 현재 버튼 상태
    bool _flag;              // 버튼이 눌렸는지 여부 추적
    unsigned long _prev_time; // 마지막 버튼 상태 변경 시간
    char _buttonMessage[50]; // 버튼 상태 메시지를 위한 C 스타일 문자열
};

// Switch 객체를 여러 개 생성
Switch mySwitch1(7);
Switch mySwitch2(6);
Switch mySwitch3(5);

void setup()
{
    Serial.begin(115200);  // 시리얼 통신 시작
}

void loop()
{
    // 각 스위치 객체에서 상태를 읽고 출력
    const char* output1 = mySwitch1.read();
    const char* output2 = mySwitch2.read();
    const char* output3 = mySwitch3.read();

    // 버튼 상태가 변경되었을 때에만 출력
    if (output1 != nullptr)
    {
        Serial.println(output1);
    }
    if (output2 != nullptr)
    {
        Serial.println(output2);
    }
    if (output3 != nullptr)
    {
        Serial.println(output3);
    }
}
