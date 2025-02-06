from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_my_robot = FindPackageShare('my_robot_simulation').find('my_robot_simulation')

    # Path to the SDF model
    sdf_model_path = PathJoinSubstitution([pkg_my_robot, 'models', 'my_robot', 'model.sdf'])

    # Spawn the robot
    spawn_robot_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'my_robot', '-file', sdf_model_path],
        output='screen'
    )

    return LaunchDescription([
        spawn_robot_node
    ])