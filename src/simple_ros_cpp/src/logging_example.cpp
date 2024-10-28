#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <chrono>
#include <iostream>
#include <functional>

using namespace std;
using namespace std::chrono_literals;

// Function declaration
bool is_divisor_of_twelve(size_t val, rclcpp::Logger logger);

class LoggerUsage : public rclcpp::Node
{
public:
    LoggerUsage()
        : Node("logger_usage_demo"), _count(0)
    {
        _pub = create_publisher<std_msgs::msg::String>("message", 10);
        _timer = create_wall_timer(1s, std::bind(&LoggerUsage::pub_callback, this));

        debug_function_to_evaluate = std::bind(is_divisor_of_twelve, std::cref(_count), get_logger());

        // Create a one-shot timer
        _one_shot_timer = create_wall_timer(5s, [this]() {
            RCLCPP_INFO(get_logger(), "One-shot timer triggered");
            _one_shot_timer->cancel(); // Cancel after it's triggered
        });
    }

private:
    int _count;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr _pub;
    rclcpp::TimerBase::SharedPtr _timer;
    rclcpp::TimerBase::SharedPtr _one_shot_timer;
    std::function<bool()> debug_function_to_evaluate;

    void pub_callback()
    {
        auto msg = std_msgs::msg::String();
        msg.data = "Current count: " + std::to_string(_count);
        
        RCLCPP_INFO(get_logger(), "Publishing: %s", msg.data.c_str());
        _pub->publish(msg);

        // Check if count is a divisor of twelve
        if (debug_function_to_evaluate())
        {
            RCLCPP_DEBUG(get_logger(), "Count is a divisor of 12");
        }

        // Check if count is even
        if (_count % 2 == 0)
        {
            RCLCPP_DEBUG(get_logger(), "Count is even!");
        }

        // Increment the count
        _count++;
        
        // Reset count if it exceeds 15
        if (_count > 15)
        {
            RCLCPP_WARN(get_logger(), "Resetting count to 0!");
            _count = 0;
        }
    }
};

bool is_divisor_of_twelve(size_t val, rclcpp::Logger logger)
{
    if (val == 0)
    {
        RCLCPP_ERROR(logger, "Module divisor cannot be 0");
        return false;
    }
    return (12 % val) == 0;
}

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LoggerUsage>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
