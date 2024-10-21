#include "simple_ros_cpp/hello_pub_class.hpp"

HellowPublisher::HellowPublisher()
    : Node("hello"), _count(0)
{
    _pub = this->create_publisher<std_msgs::msg::String>("message", 10);
    _timer = this->create_wall_timer(1s, std::bind(&HellowPublisher::printHello, this));
}

void HellowPublisher::printHello()
{
    auto msg = std_msgs::msg::String();
    msg.data = "❤️  Hello, World!!!!! " + std::to_string(_count);
    _pub->publish(msg);

    // 로그 출력
    RCLCPP_INFO(this->get_logger(), "Published: %s", msg.data.c_str());

    _count++;
}
