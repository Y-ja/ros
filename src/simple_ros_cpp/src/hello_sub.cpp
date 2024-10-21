#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <chrono>
#include <iostream>

using namespace std;
using namespace std::chrono_literals;

class HellowSubscriber : public rclcpp::Node
{
public:
    HellowSubscriber()
        : Node("hello_sub"), _count(0)  // 초기화 목록에 _count 추가
    {
        _sub = this->create_subscription<std_msgs::msg::String>(
            "message",
            10,
            std::bind(&HellowSubscriber::sub_callback, this, std::placeholders::_1));
    }

private:
    int _count;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr _sub;

    void sub_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        // 메시지를 출력하고 RCLCPP_INFO로 로깅
        RCLCPP_INFO(this->get_logger(), "Received: %s", msg->data.c_str());
        _count++;  // 수신된 메시지 수 증가 (필요에 따라 사용)
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);  // 인자 초기화
    auto node = std::make_shared<HellowSubscriber>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
