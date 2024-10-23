#include <rclcpp/rclcpp.hpp>
#include <rcl_interfaces/msg/set_parameters_result.hpp>

class SimpleParametor : public rclcpp::Node
{
public:
    SimpleParametor()
        : Node("simple_parametor")
    {
        // 파라미터 선언
        this->declare_parameter("🔧   Simple_parametor  🔧", "🔧  내가 만든 파라미터!  🔧");
        
        // 초기 파라미터 값 가져오기
        this->get_parameter("🔧   Simple_parametor  🔧", mypara_);
        
        // 파라미터 콜백 추가
        auto callback_handle = this->add_on_set_parameters_callback(
            std::bind(&SimpleParametor::parameter_callback, this, std::placeholders::_1));
        
        if (!callback_handle) {
            RCLCPP_WARN(this->get_logger(), "Failed to add parameter callback.");
        }

        // 타이머 생성
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&SimpleParametor::print_hello, this));
    }

private:
    // 타이머 콜백
    void print_hello()
    {
        RCLCPP_INFO(this->get_logger(), "parametor: %s", mypara_.c_str());
    }

    // 파라미터 콜백
    rcl_interfaces::msg::SetParametersResult parameter_callback(const std::vector<rclcpp::Parameter> &params)
    {
        rcl_interfaces::msg::SetParametersResult result;
        result.successful = true; // 성공적으로 처리됨

        for (const auto &param : params)
        {
            if (param.get_name() == "🔧   Simple_parametor  🔧")
            {
                mypara_ = param.get_value<std::string>(); // 새로운 값으로 업데이트
            }
        }
        return result;
    }

    std::string mypara_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SimpleParametor>());
    rclcpp::shutdown();
    return 0;
}
