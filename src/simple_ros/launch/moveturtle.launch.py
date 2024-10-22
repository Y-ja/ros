from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='simple_ros',  # 패키지 이름
            executable='hello_pub',  # 퍼블리셔 노드 실행 파일
            output='screen',  # 출력을 스크린에 표시
        ),
        Node(
            package='simple_ros',  # 패키지 이름
            executable='hello_sub',  # 구독자 노드 실행 파일
            output='screen',  # 출력을 스크린에 표시
        ),
        Node(
            package='simple_ros',  # MoveTurtle 클래스가 있는 패키지
            executable='move_turtle',  # MoveTurtle 노드 실행 파일
            output='screen',  # 출력을 스크린에 표시
        )
    ])
