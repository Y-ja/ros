#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"
#include <chrono>
#include <cinttypes>
#include <cstdio>
#include <string>

using namespace std;
using namespace std::chrono_literals;

class Producer : public rclcpp::Node
{
public:
    Producer(const std::string &name, const std::string &output)
        : Node(name, rclcpp::NodeOptions().use_intra_process_comms(true))
    {
        _pub = create_publisher<std_msgs::msg::Int32>(output, 10);
        
        // WeakPtr를 사용하여 퍼블리셔의 약한 참조 생성
        rclcpp::Publisher<std_msgs::msg::Int32>::WeakPtr captured_pub = _pub;

        // 퍼블리싱 콜백 람다 함수
        auto pub_callback = [captured_pub]()
        {
            auto pub_ptr = captured_pub.lock();
            if (!pub_ptr)
            {
                return; // 퍼블리셔가 더 이상 유효하지 않으면 종료
            }

            static int32_t count = 0; // 정적 변수로 카운트 유지
            auto msg = std_msgs::msg::Int32();
            msg.data = count++;

            // 메시지 및 주소 출력
            printf("Publishing msg: %d, address: 0x%" PRIXPTR "\n", msg.data, reinterpret_cast<std::uintptr_t>(&msg));
            pub_ptr->publish(std::move(msg)); // 메시지를 퍼블리시
        };

        _timer = create_wall_timer(1s, pub_callback); // 1초마다 pub_callback 호출
    }

private:
    rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr _pub;
    rclcpp::TimerBase::SharedPtr _timer;
};

class Consumer : public rclcpp::Node
{
public:
    Consumer(const std::string &name, const std::string &output)
        : Node(name, rclcpp::NodeOptions().use_intra_process_comms(true))
    {
        _sub = create_subscription<std_msgs::msg::Int32>(
            output,
            10,
            [](std_msgs::msg::Int32::UniquePtr msg)
            {
                // 수신한 메시지 및 주소 출력
                printf("Received msg value: %d, address: 0x%" PRIXPTR "\n", msg->data, reinterpret_cast<std::uintptr_t>(msg.get()));
            });
    }

private:
    rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr _sub;
};

int main(int argc, char *argv[])
{
    setvbuf(stdout, NULL, _IONBF, BUFSIZ); // 출력 버퍼링 비활성화
    rclcpp::init(argc, argv); // ROS2 초기화
    rclcpp::executors::SingleThreadedExecutor executor; // 단일 스레드 executor 생성

    // Producer와 Consumer 노드 생성
    auto producer = std::make_shared<Producer>("producer", "number");
    auto consumer = std::make_shared<Consumer>("consumer", "number");

    // executor에 노드 추가
    executor.add_node(producer);
    executor.add_node(consumer);

    executor.spin(); // executor를 사용하여 spin
    rclcpp::shutdown(); // ROS2 종료
    return 0;
}
