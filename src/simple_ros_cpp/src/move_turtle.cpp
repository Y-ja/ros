#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <turtlesim/msg/pose.hpp>

class MoveTurtle : public rclcpp::Node
{
public:
    MoveTurtle()
        : Node("move_turtle"),
          state_(State::FORWARD), // Initialize state first
          linear_velocity_(0.5),   // Set linear velocity for faster movement
          angular_velocity_(1.0),   // Set angular velocity for quicker turns
          max_velocity_(1.0),
          distance_moved_(0.0),
          turn_angle_(0.0)
    {
        // Create publisher with KeepLast QoS policy
        pub_ = this->create_publisher<geometry_msgs::msg::Twist>(
            "turtle1/cmd_vel", 
            rclcpp::QoS(rclcpp::KeepLast(10)).reliable());

        // Create subscription with KeepLast QoS policy
        sub_pose_ = this->create_subscription<turtlesim::msg::Pose>(
            "turtle1/pose",
            rclcpp::QoS(rclcpp::KeepLast(10)).reliable(),
            std::bind(&MoveTurtle::pose_callback, this, std::placeholders::_1));

        // Create timer
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&MoveTurtle::move_turtle, this));

        RCLCPP_INFO(this->get_logger(), "Starting to move in a square pattern.");
    }

private:
    enum class State { FORWARD, TURN };
    
    State state_;          // Declare state first
    double linear_velocity_;
    double angular_velocity_;
    double max_velocity_;
    double distance_moved_;
    double turn_angle_;
    
    void move_turtle()
    {
        auto twist = geometry_msgs::msg::Twist();
        
        switch (state_)
        {
            case State::FORWARD:
                // Move forward
                twist.linear.x = linear_velocity_;
                twist.angular.z = 0.0;
                distance_moved_ += linear_velocity_ * 0.1;  // Assuming timer runs every 100 ms

                if (distance_moved_ >= 2.0)  // Move forward 2 meters
                {
                    state_ = State::TURN;
                    distance_moved_ = 0.0; // Reset distance
                    RCLCPP_INFO(this->get_logger(), "Reached corner, turning 90 degrees.");
                }
                break;

            case State::TURN:
                // Turn 90 degrees
                twist.linear.x = 0.0;
                twist.angular.z = angular_velocity_;

                turn_angle_ += angular_velocity_ * 0.1;  // Update turn angle

                if (turn_angle_ >= M_PI / 2)  // 90 degrees in radians
                {
                    state_ = State::FORWARD; // Go back to moving forward
                    turn_angle_ = 0.0; // Reset turn angle
                    RCLCPP_INFO(this->get_logger(), "Finished turning, moving forward.");
                }
                break;
        }

        // Publish the twist message
        pub_->publish(twist);
    }

    void pose_callback(const turtlesim::msg::Pose::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "Received Pose: x=%.2f, y=%.2f, theta=%.2f", msg->x, msg->y, msg->theta);
    }

    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr pub_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr sub_pose_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MoveTurtle>());
    rclcpp::shutdown();
    return 0;
}
