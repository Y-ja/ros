cmake_minimum_required(VERSION 3.8)
project(tb_interface)

# Set compile options for GNU C++ or Clang compilers
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find required dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)

# Generate ROS 2 service interface files
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/ServoAngle.srv"  # Path to the service file
  DEPENDENCIES builtin_interfaces  # Required dependencies (builtin interfaces)
)

# Set up testing environment if testing is enabled
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# Export runtime dependencies for ROS 2 and finalize package build
ament_export_dependencies(rosidl_default_runtime)
ament_package()
