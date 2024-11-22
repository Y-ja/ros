#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <chrono>
#include <iostream>

using namespace std;
using namespace std::chrono_literals;

class SyncAsyncWriter : public rclcpp::Node
{
public:
    explicit SyncAsyncWriter()
        : Node("sync_async_pub"), _count(0)
    {
        _pub_sync = create_publisher<std_msgs::msg::String>("sync_topic", 10);
        _pub_async = create_publisher<std_msgs::msg::String>("async_topic", 10);
        _timer = create_wall_timer(1s, std::bind(&SyncAsyncWriter::pub_callback, this));
    }

private:
    int _count;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr _pub_sync;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr _pub_async;
    rclcpp::TimerBase::SharedPtr _timer;
    
    void pub_callback()
    {
        auto msg = std_msgs::msg::String();
        
        // Synchronously publishing
        msg.data = "Synchronously publishing: Hello, World!!!!! " + to_string(_count);
        _pub_sync->publish(msg);
        RCLCPP_INFO(get_logger(), msg.data.c_str());
        
        // Asynchronously publishing
        msg.data = "Asynchronously publishing: Hello, World!!!!! " + to_string(_count);
        _pub_async->publish(msg);
        RCLCPP_INFO(get_logger(), msg.data.c_str());
        
        _count++;
    }
};

int main()
{
    rclcpp::init(0, nullptr);
    auto node = std::make_shared<SyncAsyncWriter>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
