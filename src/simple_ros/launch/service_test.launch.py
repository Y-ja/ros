from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='simple_ros',  # 패키지 이름
            executable='hello_pub',  # 서비스 서버 노드
            name='service_server',  # 노드 이름 설정
            output='screen',  # 출력 설정
        ),
        Node(
            package='simple_ros',  # 패키지 이름
            executable='hello_sub',  # 서비스 클라이언트 노드
            name='service_client',  # 노드 이름 설정
            output='screen',  # 출력 설정
        )
    ])
