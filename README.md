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
