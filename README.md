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
