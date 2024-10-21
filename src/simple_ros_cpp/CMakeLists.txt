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

# Include directories
include_directories(include)  # Add include directory for headers

# Create executable for hello_pub
add_executable(hello_pub src/hello_pub.cpp)
ament_target_dependencies(hello_pub rclcpp std_msgs)  # Link required dependencies

# Create executable for hello_pub_class
add_executable(hello_pub_class src/hello_pub_class.cpp src/hello_pub_class_method.cpp)
ament_target_dependencies(hello_pub_class rclcpp std_msgs)  # Link required dependencies

# Create executable for hello_pub_lambda
add_executable(hello_pub_lambda src/hello_pub_lambda.cpp)
ament_target_dependencies(hello_pub_lambda rclcpp std_msgs)  # Link required dependencies

# Create executable for hello_sub
add_executable(hello_sub src/hello_sub.cpp)  # Add hello_sub executable
ament_target_dependencies(hello_sub rclcpp std_msgs)  # Link required dependencies

# Install the executables
install(TARGETS
  hello_pub
  hello_pub_class
  hello_pub_lambda
  hello_sub  # Include hello_sub in the install targets
  DESTINATION lib/${PROJECT_NAME}  # Install to the library directory of the package
)

# Install launch directory
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})  # Corrected keyword

# Testing and linting
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)  # Find linting tools
  set(ament_cmake_copyright_FOUND TRUE)  # Enable copyright checking
  set(ament_cmake_cpplint_FOUND TRUE)  # Enable cpplint checking
  ament_lint_auto_find_test_dependencies()  # Find test dependencies automatically
endif()

# Package the project
ament_package()  # Finalize the package
