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
