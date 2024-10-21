#include <iostream>
#include <chrono>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std;
using namespace std::chrono_literals;

void printHello(); // 함수 선언

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("hello");
    static int count = 0; // count 변수를 여기서 정의

    // 퍼블리셔 생성
    auto pub = node->create_publisher<std_msgs::msg::String>("message", 10);
    
    auto timer = node->create_wall_timer(1s, [&]() {
        auto msg = std_msgs::msg::String();
        msg.data = "Hello ❤️  ->   " + to_string(count); // 메시지 설정
        pub->publish(msg); // 메시지 퍼블리시
        printHello(); // printHello 함수 호출
        count++; // 카운트 증가
    });

    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}

void printHello() {
    static int count = 0; // 카운트 변수를 여기서 정의
    cout << "Hello ❤️  ->   " << count << endl;
    count++;
}
