#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

class MyRobotController : public rclcpp::Node
{
public:
    MyRobotController() : Node("my_robot_controller")
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&MyRobotController::timer_callback, this));
    }

private:
    void timer_callback()
    {
        auto message = geometry_msgs::msg::Twist();
        message.linear.x = 0.5;  // Move forward at 0.5 m/s
        message.angular.z = 0.2; // Rotate at 0.2 rad/s
        publisher_->publish(message);
    }

    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyRobotController>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}