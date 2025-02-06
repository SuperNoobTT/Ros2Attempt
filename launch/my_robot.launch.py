import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_gazebo_ros = FindPackageShare('gazebo_ros').find('gazebo_ros')
    pkg_my_robot = FindPackageShare('my_robot_simulation').find('my_robot_simulation')

    # Path to the world file
    world_file = PathJoinSubstitution([pkg_my_robot, 'worlds', 'empty_world.sdf'])

    # Launch Gazebo
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file}.items()
    )

    # Spawn the robot
    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_my_robot, 'launch', 'spawn_robot.launch.py')
        )
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value=world_file,
            description='Path to the world file'
        ),
        gazebo_launch,
        spawn_robot
    ])