cmake_minimum_required(VERSION 3.8)
project(user_interface)

# C++ 컴파일러에 대한 경고 옵션 설정
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 의존성 찾기
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)

# 메시지 및 서비스 파일로부터 인터페이스 생성
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/UserInt.msg"
  "srv/AddAndOdd.srv"
  DEPENDENCIES builtin_interfaces  # 의존성 명시
)

# 테스트 빌드를 위한 설정
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)  # 저작권 확인 건너뛰기
  set(ament_cmake_cpplint_FOUND TRUE)    # cpplint 건너뛰기
  ament_lint_auto_find_test_dependencies()
endif()

# 패키지에서 필요한 런타임 의존성 내보내기
ament_export_dependencies(rosidl_default_runtime)

# 패키지 정의
ament_package()
