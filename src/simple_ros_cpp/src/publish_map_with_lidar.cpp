#include "nav_msgs/msg/occupancy_grid.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "rclcpp/rclcpp.hpp"
#include <chrono>
#include <cmath>  // For atan2, cos, sin

using namespace std;
using namespace std::chrono_literals;

class PublishMap : public rclcpp::Node
{
public:
    explicit PublishMap()
        : Node("publish_map_with_lidar"), _count(0), _row(0)
    {
        _pub = create_publisher<nav_msgs::msg::OccupancyGrid>("map", 10);

        // Odometry Subscription
        _odom_sub = create_subscription<nav_msgs::msg::Odometry>(
            "odom", 10, [this](const nav_msgs::msg::Odometry::SharedPtr msg) {
                _odom = *msg;
            });

        // LaserScan Subscription
        rclcpp::QoS rmw_qos_profile_sensor_data = rclcpp::SensorDataQoS();
        _laser_sub = create_subscription<sensor_msgs::msg::LaserScan>(
            "scan", rmw_qos_profile_sensor_data, [this](const sensor_msgs::msg::LaserScan::SharedPtr msg) {
                _laser = *msg;
            });

        // Timer for periodic map publishing
        _timer = create_wall_timer(1ms, std::bind(&PublishMap::pub_callback, this));

        // Map info setup
        _msg.info.resolution = 0.1f;
        _msg.info.width = 100;
        _msg.info.height = 100;
        _msg.info.origin.position.x = -(_msg.info.width * _msg.info.resolution) / 2;
        _msg.info.origin.position.y = -(_msg.info.height * _msg.info.resolution) / 2;
        _msg.info.origin.position.z = 0;
        _msg.info.origin.orientation.x = 0;
        _msg.info.origin.orientation.y = 0;
        _msg.info.origin.orientation.z = 0;
        _msg.info.origin.orientation.w = 1;

        _msg.data.resize(_msg.info.width * _msg.info.height, -1);  // Initialize all grid cells to -1

        // Mark the center of the map (optional, center of the grid)
        mark_center();
    }

private:
    unsigned int _count;
    unsigned int _row;
    rclcpp::Publisher<nav_msgs::msg::OccupancyGrid>::SharedPtr _pub;
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr _odom_sub;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr _laser_sub;
    rclcpp::TimerBase::SharedPtr _timer;
    nav_msgs::msg::OccupancyGrid _msg;
    nav_msgs::msg::Odometry _odom;
    sensor_msgs::msg::LaserScan _laser;

    void pub_callback()
    {
        static int value = 0;
        _msg.header.frame_id = "odom";
        _msg.header.stamp = get_clock()->now();

        // Odometry: Robot position and orientation
        float robot_x = _odom.pose.pose.position.x;
        float robot_y = _odom.pose.pose.position.y;
        float robot_yaw = atan2(
            2 * (_odom.pose.pose.orientation.w * _odom.pose.pose.orientation.z +
                 _odom.pose.pose.orientation.x * _odom.pose.pose.orientation.y),
            1 - 2 * (_odom.pose.pose.orientation.y * _odom.pose.pose.orientation.y +
                     _odom.pose.pose.orientation.z * _odom.pose.pose.orientation.z)
        );

        // Iterate through each laser scan range
        int iter = 0;
        for (auto& scan_radian : _laser.ranges)
        {
            if (scan_radian == INFINITY || scan_radian == 0.0)
            {
                scan_radian = _laser.range_max;  // If invalid, use max range
            }

            // Compute the angle of each laser scan point
            float scan_theta = _laser.angle_min + _laser.angle_increment * iter;

            // Convert laser scan to map coordinates
            float scan_x = robot_x + scan_radian * cos(robot_yaw + scan_theta);
            float scan_y = robot_y + scan_radian * sin(robot_yaw + scan_theta);
 
            // Convert map coordinates to grid indices
            int map_x = static_cast<int>((scan_x - _msg.info.origin.position.x) / _msg.info.resolution);
            int map_y = static_cast<int>((scan_y - _msg.info.origin.position.y) / _msg.info.resolution);

            // Check if the point is within the map bounds
            if (map_x >= 0 && map_x < _msg.info.width && map_y >= 0 && map_y < _msg.info.height)
            {
                _msg.data[map_y * _msg.info.width + map_x] = 100;  // Mark the map cell as occupied
            }

            iter++;
        }

        // Publish the updated map
        _pub->publish(_msg);
    }

    // Function to mark the center of the map (can be used to display the center of the map)
    void mark_center()
    {
        int center_x = _msg.info.width / 2;
        int center_y = _msg.info.height / 2;

        // Mark the center with a unique value (e.g., 50) to visualize it
        _msg.data[center_y * _msg.info.width + center_x] = 50;  // 50 can represent the center point
    }
};

int main()
{
    rclcpp::init(0, nullptr);
    auto node = std::make_shared<PublishMap>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
