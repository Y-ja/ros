from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='simple_ros',  # Package name for the publisher
            executable='hello_pub',  # Publisher node executable
            output='screen',  # Display output on the screen
        ),
        Node(
            package='simple_ros',  # Package name for the subscriber
            executable='hello_sub',  # Subscriber node executable
            output='screen',  # Display output on the screen
        ),
        Node(
            package='simple_ros',  # Package name for MoveTurtle
            executable='move_turtle',  # MoveTurtle node executable
            output='screen',  # Display output on the screen
        )
    ])
