#include "lifecycle_msgs/msg/state.hpp"
#include "lifecycle_msgs/msg/transition.hpp"
#include "lifecycle_msgs/srv/change_state.hpp"
#include "lifecycle_msgs/srv/get_state.hpp"

#include "rclcpp/rclcpp.hpp"
#include <chrono>
#include <iostream>

using namespace std;
using namespace std::chrono_literals;

class LifecycleServiceClient : public rclcpp::Node
{
public:
    LifecycleServiceClient()
        : Node("lifecycle_service_client")  // Node name
    {
        _client = create_client<lifecycle_msgs::srv::ChangeState>("lc_talker/change_state");

        // Wait for the service to be available
        while (!_client->wait_for_service(1s))
        {
            RCLCPP_INFO(get_logger(), "Service not available, waiting...");
        }
        _send_timer = create_wall_timer(3s, std::bind(&LifecycleServiceClient::send_request, this));
    }

private:
    rclcpp::Client<lifecycle_msgs::srv::ChangeState>::SharedPtr _client;
    rclcpp::TimerBase::SharedPtr _send_timer;

    void send_request()
    {
        _send_timer->cancel();  // Cancel the timer

        auto _request = std::make_shared<lifecycle_msgs::srv::ChangeState::Request>();
        
        // Request to transition to CONFIGURE state
        _request->transition.id = lifecycle_msgs::msg::Transition::TRANSITION_CONFIGURE;
        
        auto future = _client->async_send_request(_request,
                                                  std::bind(&LifecycleServiceClient::done_callback,
                                                            this,
                                                            std::placeholders::_1));

        // Wait for the request result
        future.wait();

        if (future.get()->success) {
            RCLCPP_INFO(get_logger(), "Configure Successful");
            
            // Request to transition to ACTIVATE state
            _request->transition.id = lifecycle_msgs::msg::Transition::TRANSITION_ACTIVATE;  // Update transition ID
            future = _client->async_send_request(_request,
                                                  std::bind(&LifecycleServiceClient::done_callback,
                                                            this,
                                                            std::placeholders::_1));
            future.wait();  // Wait for the result again
        } else {
            RCLCPP_INFO(get_logger(), "Configure Error");
        }                                                    
    }

    void done_callback(rclcpp::Client<lifecycle_msgs::srv::ChangeState>::SharedFuture future)
    {
        auto response = future.get();
        RCLCPP_INFO(get_logger(), "Success: %s", response->success ? "true" : "false");
    }
};

int main(int argc, char *argv[])
{
    setvbuf(stdout, NULL, _IONBF, BUFSIZ);
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LifecycleServiceClient>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
