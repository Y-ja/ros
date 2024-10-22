cmake_minimum_required(VERSION 3.8)
project(simple_ros_cpp)

# Compiler warnings
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)  # Enable all warnings
endif()

# Find required packages
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)  # ROS 2 C++ client library
find_package(std_msgs REQUIRED)  # Standard messages for ROS 2
find_package(geometry_msgs REQUIRED)  # Geometry messages
find_package(turtlesim REQUIRED)  # Turtlesim package
find_package(OpenCV REQUIRED)  # OpenCV library

# Include directories
include_directories(include)  # Add include directory for headers

# Create executables
add_executable(hello_pub src/hello_pub.cpp)
ament_target_dependencies(hello_pub rclcpp std_msgs)  # Link dependencies for hello_pub
target_link_libraries(hello_pub ${OpenCV_LIBS})  # Link OpenCV to hello_pub

add_executable(hello_pub_class src/hello_pub_class.cpp src/hello_pub_class_method.cpp)
ament_target_dependencies(hello_pub_class rclcpp std_msgs)  # Link dependencies for hello_pub_class
target_link_libraries(hello_pub_class ${OpenCV_LIBS})  # Link OpenCV to hello_pub_class

add_executable(hello_pub_lambda src/hello_pub_lambda.cpp)
ament_target_dependencies(hello_pub_lambda rclcpp std_msgs)  # Link dependencies for hello_pub_lambda
target_link_libraries(hello_pub_lambda ${OpenCV_LIBS})  # Link OpenCV to hello_pub_lambda

add_executable(hello_sub src/hello_sub.cpp)  # Create hello_sub executable
ament_target_dependencies(hello_sub rclcpp std_msgs)  # Link dependencies for hello_sub
target_link_libraries(hello_sub ${OpenCV_LIBS})  # Link OpenCV to hello_sub

add_executable(hello_sub_opencv src/hello_sub_opencv.cpp)  # Create hello_sub_opencv executable
ament_target_dependencies(hello_sub_opencv rclcpp std_msgs)  # Link dependencies for hello_sub_opencv
target_link_libraries(hello_sub_opencv ${OpenCV_LIBS})  # Link OpenCV to hello_sub_opencv

add_executable(move_turtle src/move_turtle.cpp)
ament_target_dependencies(move_turtle rclcpp geometry_msgs turtlesim)  # Correctly link dependencies for move_turtle
target_link_libraries(move_turtle ${OpenCV_LIBS})  # Link OpenCV if used

# Install the executables
install(TARGETS
  hello_pub
  hello_pub_class
  hello_pub_lambda
  hello_sub
  hello_sub_opencv
  move_turtle  # Added move_turtle to installation
  DESTINATION lib/${PROJECT_NAME}  # Install to the library directory of the package
)

# Install launch directory
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})  # Install launch files

# Testing and linting
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)  # Find linting tools
  set(ament_cmake_copyright_FOUND TRUE)  # Enable copyright checking
  set(ament_cmake_cpplint_FOUND TRUE)  # Enable cpplint checking
  ament_lint_auto_find_test_dependencies()  # Find test dependencies automatically
endif()

# Package the project
ament_package()  # Finalize the package
