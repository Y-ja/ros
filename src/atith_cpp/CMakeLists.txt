cmake_minimum_required(VERSION 3.8)
project(atith_cpp)

# Set C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(user_interface REQUIRED)

# Include directories
include_directories(include)

# Add executable for the argument node
add_executable(argument src/arithmetic/argument.cpp)
ament_target_dependencies(argument rclcpp user_interface)

# Add executable for the calculator node
add_executable(calculator src/calculator/main.cpp src/calculator/calculator.cpp)  # Fixed path
ament_target_dependencies(calculator rclcpp user_interface)

# Install the nodes
install(TARGETS
  argument
  calculator
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch and param directories
install(DIRECTORY
  launch/
  param/
  DESTINATION share/${PROJECT_NAME}
)

# Uncomment the following section to fill in further dependencies manually
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # Skip the linter that checks for copyrights if not yet added
  set(ament_cmake_copyright_FOUND TRUE)
  # Skip cpplint (only works in a git repo) if not yet added
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
