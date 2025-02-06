cmake_minimum_required(VERSION 3.5)
project(my_robot_simulation)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)

add_executable(my_robot_controller src/my_robot_controller.cpp)
ament_target_dependencies(my_robot_controller rclcpp geometry_msgs)

install(TARGETS
  my_robot_controller
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY
  launch
  models
  DESTINATION share/${PROJECT_NAME})

ament_package()