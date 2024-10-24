#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "user_interface/action/fibonacci.hpp"
#include <chrono>
#include <iostream>
#include <thread>

using namespace std;
using namespace std::placeholders;
using namespace std::chrono_literals;

class ActionServer : public rclcpp::Node
{
public:
    ActionServer()
        : Node("action_server")
    {
        _action_server = rclcpp_action::create_server<Fibonacci>(
            this, "fibonacci",
            std::bind(&ActionServer::handle_goal, this, _1, _2),
            std::bind(&ActionServer::handle_cancel, this, _1),
            std::bind(&ActionServer::handle_accepted, this, _1));
    }

private:
    typedef user_interface::action::Fibonacci Fibonacci;
    typedef rclcpp_action::ServerGoalHandle<Fibonacci> GoalHandleFibonacci;
    rclcpp_action::Server<Fibonacci>::SharedPtr _action_server;

    rclcpp_action::GoalResponse handle_goal(
        const rclcpp_action::GoalUUID &uuid,
        std::shared_ptr<const Fibonacci::Goal> goal)
    {
        RCLCPP_INFO(get_logger(), "Requested step: %d", goal->step);
        (void)uuid;
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
    }

    rclcpp_action::CancelResponse handle_cancel(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
    {
        RCLCPP_INFO(get_logger(), "Canceling goal");
        (void)goal_handle;
        return rclcpp_action::CancelResponse::ACCEPT;
    }

    void handle_accepted(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
    {
        std::thread{std::bind(&ActionServer::execute, this, goal_handle)}.detach();
    }

    void execute(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
    {
        RCLCPP_INFO(get_logger(), "Executing goal");
        const auto goal = goal_handle->get_goal();

        auto feedback = std::make_shared<Fibonacci::Feedback>();
        feedback->temp_seq.push_back(0);
        if (goal->step > 0) {
            feedback->temp_seq.push_back(1);
        }

        goal_handle->publish_feedback(feedback);

        for (size_t i = 2; i < static_cast<size_t>(goal->step); ++i) {  // 수정된 부분
            int next_number = feedback->temp_seq[i - 1] + feedback->temp_seq[i - 2];
            feedback->temp_seq.push_back(next_number);
            goal_handle->publish_feedback(feedback);
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }

        auto result = std::make_shared<Fibonacci::Result>();
        result->seq = feedback->temp_seq;
        goal_handle->succeed(result);
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ActionServer>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
