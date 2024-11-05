# ROS (Robot Operating System) 🦾🤖

## 소개

ROS는 로봇 응용 프로그램을 개발하기 위한 오픈 소스 프레임워크입니다. 다양한 로봇 하드웨어와 소프트웨어를 통합하고, 재사용 가능한 코드 패키지를 제공하여 로봇 소프트웨어의 개발을 촉진합니다.

## 주요 특징

- **모듈화**: ROS는 여러 개의 패키지로 구성되어 있어, 각 기능을 독립적으로 개발하고 사용할 수 있습니다.
- **통신**: ROS는 메시지 기반의 통신을 지원하여, 다양한 노드 간의 데이터 전송을 쉽게 처리할 수 있습니다.
- **도구 지원**: 로봇 시뮬레이션, 시각화, 디버깅 등을 위한 다양한 도구를 제공합니다.

## 설치

ROS를 설치하려면 다음 단계를 따르세요:

1. **시스템 요구사항**: Ubuntu 20.04 또는 22.04를 사용해야 합니다.
2. **패키지 목록 업데이트**:
 ```bash
   sudo apt update
   sudo apt upgrade
 ```

## ROS 설치
 ```bash
 sudo apt install ros-noetic-desktop-full

 ```

## 환경 설정
 ```bash
 source /opt/ros/noetic/setup.bash
 ```

## 워크스페이스 생성
 ```bash
 mkdir -p ~/catkin_ws/src
 cd ~/catkin_ws/
 catkin_make

 ```
## 패키지 생성
 ```bash
 cd src
 catkin_create_pkg my_package std_msgs rospy roscpp

 ```

## 노드 실행
 ```bash
 rosrun my_package my_node
 ```

## 간단한 예시코드
 ```bash
 /usr/bin/env python
 ```
 ``` bash
 import rospy
 from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

 ``` 


# ROS2 실습 정리 📚

## 1부: ROS2 CLI 실습 🚀
### 명령어 실습
- **`ros2 run`**
  - **설명**: 지정된 패키지의 노드를 실행합니다.
  - **예시**: 
    ```bash
    ros2 run my_package my_node
    ```

- **`ros2 launch`**
  - **설명**: 여러 노드를 동시에 실행하는 런치 파일을 실행합니다.
  - **예시**:
    ```bash
    ros2 launch my_package my_launch_file.launch.py
    ```

- **`ros2 topic`**
  - **설명**: 토픽을 관리합니다. 생성, 삭제, 메시지 확인 등이 가능합니다.
  - **예시**:
    ```bash
    ros2 topic list
    ```

- **`ros2 node`**
  - **설명**: 현재 실행 중인 노드의 정보를 확인합니다.
  - **예시**:
    ```bash
    ros2 node list
    ```

- **`ros2 param`**
  - **설명**: 노드의 파라미터를 설정하고 조회합니다.
  - **예시**:
    ```bash
    ros2 param list
    ```

- **`ros2 service`**
  - **설명**: 서비스를 호출하거나 확인합니다.
  - **예시**:
    ```bash
    ros2 service call /my_service std_srvs/srv/Empty
    ```

- **`ros2 action`**
  - **설명**: 액션 서버와 클라이언트를 관리합니다.
  - **예시**:
    ```bash
    ros2 action list
    ```

## 2부: ROS2 RQT 실습 📊
### RQT 도구 활용
- **`rqt_graph`**
  - **설명**: ROS 시스템의 노드 및 토픽 관계를 시각화합니다.
  - **예시**:
    ```bash
    rqt_graph
    ```

- **`rqt_plot`**
  - **설명**: 실시간 데이터를 그래프로 시각화합니다.
  - **예시**:
    ```bash
    rqt_plot /my_topic/data
    ```

- **`rqt_image_view`**
  - **설명**: 이미지 토픽을 시각화하여 확인합니다.
  - **예시**:
    ```bash
    rqt_image_view
    ```

- **`rqt_console`**
  - **설명**: ROS 로그 메시지를 필터링하고 확인합니다.
  - **예시**:
    ```bash
    rqt_console
    ```

- **`rqt_logger_level`**
  - **설명**: 노드의 로깅 레벨을 설정합니다.
  - **예시**:
    ```bash
    rqt_logger_level
    ```

## 3부: 패키지 및 노드 작성 🛠️
### 패키지 생성
- **`ros2 pkg create`**
  - **설명**: 새로운 ROS2 패키지를 생성합니다.
  - **예시**:
    ```bash
    ros2 pkg create my_new_package
    ```

### 2024_10_18
- **기본 노드 코드 작성**
  - **예시**: 간단한 퍼블리셔 노드
    ```python
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String

    class MyPublisher(Node):
        def __init__(self):
            super().__init__('my_publisher')
            self.publisher_ = self.create_publisher(String, 'my_topic', 10)
            self.timer = self.create_timer(1.0, self.timer_callback)

        def timer_callback(self):
            msg = String()
            msg.data = 'Hello, ROS2!'
            self.publisher_.publish(msg)

    def main(args=None):
        rclpy.init(args=args)
        node = MyPublisher()
        rclpy.spin(node)
        rclpy.shutdown()

    if __name__ == '__main__':
        main()
    ```

### 2024_10_21
- **C++ 패키지 생성**
  - **설명**: C++로 ROS2 패키지를 생성하고 CMake 설정을 작성합니다.
  - **예시**:
    ```bash
    ros2 pkg create simple_ros_cpp --build-type ament_cmake
    ```

- **CMakeLists.txt**:
  ```cmake
  cmake_minimum_required(VERSION 3.5)
  project(simple_ros_cpp)

  find_package(ament_cmake REQUIRED)
  find_package(rclcpp REQUIRED)

  add_executable(my_cpp_publisher src/my_cpp_publisher.cpp)
  ament_target_dependencies(my_cpp_publisher rclcpp)

  install(TARGETS
    my_cpp_publisher
    DESTINATION lib/${PROJECT_NAME}
  )

  ament_package()
```



# ROS2 실습 정리 📚

## 2024_10_22
### 서비스 작성
- **예시**: 간단한 서비스 서버
```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class AddTwoIntsServer(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_callback)

    def add_callback(self, request, response):
        response.sum = request.a + request.b
        return response

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 2024_10_23
### 파라미터 적용 노드 작성
- 예시: 파라미터를 사용하는 노드

```python
class MyParameterNode(Node):
    def __init__(self):
        super().__init__('my_parameter_node')
        self.declare_parameter('my_param', 'default_value')
        param_value = self.get_parameter('my_param').value
        self.get_logger().info(f'Parameter value: {param_value}')

```

## 2024_10_28
### 심화 프로그래밍: 로깅 📝
- 설명: 로깅 환경 변수를 설정하고 노드를 작성합니다.
```python
import rclpy
from rclpy.node import Node

class MyLoggingNode(Node):
    def __init__(self):
        super().__init__('my_logging_node')
        self.get_logger().info('This is an info message.')

def main(args=None):
    rclpy.init(args=args)
    node = MyLoggingNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

```




### 터틀봇3 설명 🤖

터틀봇3는 ROS2(로봇 운영 체제 2) 기반의 로봇 플랫폼으로, 로봇 연구 및 교육에 적합한 다양한 기능을 제공합니다. 이 로봇은 자율 주행, 물체 인식, 매핑 및 탐색 등의 기능을 수행할 수 있습니다. 터틀봇3는 특히 저렴하고 유연성이 뛰어나기 때문에 로봇 개발자와 연구자에게 인기 있는 선택입니다.

#### 특징 🌟
- **모듈화된 디자인**: 부품이 쉽게 교체 가능하여 사용자 맞춤형 로봇 제작이 가능합니다.
- **고성능 센서**: LiDAR, 카메라, IMU 센서 등을 통해 환경 인식 및 매핑 기능을 지원합니다.
- **ROS2 지원**: ROS2를 통해 강력한 소프트웨어 생태계를 활용할 수 있습니다.
- **교육용 플랫폼**: 로봇 공학 및 AI 교육에 적합하여 많은 교육기관에서 사용되고 있습니다.

#### 데이터 계통 및 전력 계통 ⚡
- **데이터 계통**: 터틀봇3는 센서와 모터 간의 데이터 통신을 위한 여러 인터페이스(예: UART, I2C, SPI)를 지원합니다.
- **전력 계통**: 배터리를 사용하며, 배터리 잔량 모니터링 기능이 포함되어 있습니다. 전원 관리가 효율적입니다.

#### 예시 코드 📝
터틀봇3의 기본 동작을 보여주는 예시 코드입니다. 아래 코드는 ROS2를 사용하여 터틀봇3를 전진시키는 간단한 Publisher 노드를 작성한 것입니다.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Turtlebot3Move(Node):
    def __init__(self):
        super().__init__('turtlebot3_move')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.2  # 전진 속도
        msg.angular.z = 0.0  # 회전 속도
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: linear.x: %f, angular.z: %f' % (msg.linear.x, msg.angular.z))

def main(args=None):
    rclpy.init(args=args)
    turtlebot3_move = Turtlebot3Move()
    rclpy.spin(turtlebot3_move)
    turtlebot3_move.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```


# 🛡️ ROS2 보안: SROS2 🔐
## 📚 소개
SROS2 (Secure ROS2)는 ROS2 시스템에서 보안을 강화하기 위한 확장입니다. 로봇 시스템에서 데이터 보호, 인증, 권한 부여, 무결성 검사 등을 제공하여 민감한 정보와 시스템을 보호하는 데 사용됩니다. SROS2는 DDS (Data Distribution Service)의 보안 확장을 활용합니다.

## 🌟 주요 기능

  ### 🔒 데이터 암호화
   SROS2는 로봇 시스템 내에서 송수신되는 메시지를 암호화하여 데이터 유출을 방지합니다.

  ### 🛂 인증
    사용자는 시스템에 연결하기 위해 인증을 받아야 하며, 인증된 사용자만 서비스에 접근할 수 있습니다.

  ### 🛡️ 무결성 검사
   전송되는 데이터가 변조되지 않도록 보호하며, 데이터가 중간에 변경되었을 경우 이를 감지합니다.

  ### 🔑 권한 부여
   특정 사용자나 프로세스에 대해 권한을 부여하여 시스템 내에서 누가 어떤 작업을 수행할 수 있는지 제어합니다.

  ### 📡 DDS 보안 확장
   DDS의 보안 기능을 사용하여 통신을 보호합니다. DDS는 데이터 전송에 있어 보안, 성능, 확장성을 제공하는 미들웨어로, SROS2는 이를 확장하여 더욱 강력한 보안을 구현합니다.

## 🛠️ SROS2 설정 방법
### 1️⃣ ROS2 보안 패키지 설치 

```bash
sudo apt install ros-foxy-sros2
```  

## 2️⃣ 보안 설정 파일 생성

- SROS2는 보안을 위한 여러 설정을 JSON 파일 형식으로 관리합니다. 다음은 기본 보안 설정을 위한 예시 파일입니다.

- ~/.ros2/security/pki 디렉토리를 생성합니다.

```bash
mkdir -p ~/.ros2/security/pki
```
- 이 디렉토리에 인증서와 키 파일을 배치합니다.

## 3️⃣ 보안 인증서 생성

- SROS2는 보안을 위해 인증서를 사용합니다. OpenSSL을 이용하여 인증서를 생성할 수 있습니다.

```bash
openssl req -new -newkey rsa:2048 -days 365 -nodes -keyout mykey.key -out mycert.crt

```

- 이렇게 생성된 인증서와 키는 각각 mykey.key와 mycert.crt로 저장됩니다.

## 4️⃣ 보안 설정을 적용한 실행

- ROS2 노드를 실행할 때, 보안 설정을 적용하려면 다음과 같이 실행할 수 있습니다.

```bash
export ROS_SECURITY_ROOT_DIRECTORY=~/.ros2/security
export ROS_SECURITY_ENABLE=true
export ROS_SECURITY_STRATEGY=Enforce
ros2 run my_package my_secure_node

```

- ROS_SECURITY_ENABLE=true: 보안을 활성화합니다.
- ROS_SECURITY_STRATEGY=Enforce: 보안 정책을 강제합니다. 이 설정을 통해 인증되지 않은 연결을 차단합니다.


## 5️⃣ 인증서 교환 및 인증

SROS2 시스템에서 실행되는 노드들은 인증서와 키를 통해 서로 인증을 수행합니다. 이 과정을 통해 노드는 신뢰할 수 있는 방식으로 통신을 할 수 있게 됩니다.

## 6️⃣ 인증되지 않은 사용자 접근 차단

SROS2는 사용자 인증을 통해 권한을 제어합니다. 예를 들어, 인증되지 않은 사용자가 시스템에 접근하려 하면, 인증 절차가 거쳐지기 전까지 통신이 차단됩니다. 이를 통해 시스템 보안이 강화됩니다.

## 🔐 SROS2 보안 전략

  ## 💪 Enforce (강제)
  보안을 반드시 활성화해야 하며, 인증되지 않은 노드는 통신을 할 수 없습니다.

  ## 🚫 Disable (비활성화)
  보안 기능을 비활성화하여 보안 없이 ROS2 노드를 실행합니다.

  ## 🔍 Verify (검증)
  보안 검증을 수행하되, 인증되지 않은 노드는 통신할 수 있습니다.

## 👨‍💻 예시: SROS2로 보안된 통신

### 노드 생성 (SecurityNode)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SecurityNode(Node):
    def __init__(self):
        super().__init__('security_node')
        self.publisher_ = self.create_publisher(String, 'secure_topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = "Secure Message"
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = SecurityNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

```

```cpp 
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class SecurityNode : public rclcpp::Node
{
public:
    SecurityNode() : Node("security_node")
    {
        // Publisher 생성
        publisher_ = this->create_publisher<std_msgs::msg::String>("secure_topic", 10);
        // 타이머 설정: 1초마다 콜백 실행
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1), std::bind(&SecurityNode::timer_callback, this));
    }

private:
    void timer_callback()
    {
        auto msg = std_msgs::msg::String();
        msg.data = "Secure Message";  // 보안 메시지
        publisher_->publish(msg);    // 메시지 발행
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str());
    }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);  // ROS2 초기화
    rclcpp::spin(std::make_shared<SecurityNode>());  // 노드 실행
    rclcpp::shutdown();  // ROS2 종료
    return 0;
}

```
- 보안을 활성화하여 실행하려면, 위에서 설명한 것처럼 환경 변수를 설정해야 합니다.

```bash
export ROS_SECURITY_ENABLE=true
export ROS_SECURITY_ROOT_DIRECTORY=~/.ros2/security
ros2 run my_package security_node
```

## ⚠️ SROS2 사용 시 고려사항

### 🚶‍♂️ 성능
보안 기능을 활성화하면 시스템 성능에 영향을 미칠 수 있습니다. 따라서, 보안을 활성화한 상태에서의 성능을 측정하여 최적화가 필요할 수 있습니다.

### 🔑 인증서 관리
인증서의 유효 기간 관리와, 인증서 갱신 및 폐기 절차가 중요합니다. 로봇 시스템이 장기적으로 안전하게 운영될 수 있도록 관리해야 합니다.

### 🔗 호환성
SROS2는 ROS2의 다양한 버전에서 지원되므로, 사용하는 ROS2 버전과의 호환성도 체크해야 합니다.


