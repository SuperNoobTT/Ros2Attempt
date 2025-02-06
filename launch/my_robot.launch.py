from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    world_file_path = PathJoinSubstitution([FindPackageShare('my_robot_simulation'), 'worlds', 'empty_world.sdf'])
    print(f"World file path: {world_file_path}")
    return LaunchDescription([
        # Set Gazebo resource path (optional, if you have custom models)
        SetEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            PathJoinSubstitution([FindPackageShare('my_robot_simulation'), 'models'])
        ),

        # Declare the world file argument
        DeclareLaunchArgument(
            'world_file',
            default_value=PathJoinSubstitution([FindPackageShare('my_robot_simulation'), 'worlds', 'empty_world.sdf']),
            description='Path to the world file to load into Gazebo'
        ),

        # Launch Gazebo using ros_gz_sim
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
                ])
            ),
            launch_arguments={
                'gz_args': [LaunchConfiguration('world_file')],
                'on_exit_shutdown': 'True'
            }.items(),
        ),

        # Spawn the robot
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('my_robot_simulation'), 'launch', 'spawn_robot.launch.py'
                ])
            )
        ),
    ])
