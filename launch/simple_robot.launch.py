import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ros_gz_bridge.actions import RosGzBridge
from launch_ros.actions import Node

def generate_launch_description():
    pkg_path = get_package_share_directory('simple_robot')
    pkg_ros_gz = get_package_share_directory('ros_gz_sim')
    
    robot_file = PathJoinSubstitution([
        pkg_path,
        "model/simple_robot.xacro"
    ])
    # World path using proper substitution
    world_path = PathJoinSubstitution([
        pkg_path,
        'worlds/simple_world.sdf'
    ])

    with open(robot_file, "r") as infp:
        robot_desc = infp.read()

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        arguments=[sdf_file],
        output=['screen']
    )

    gz_sim = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    pkg_ros_gz,
                    'launch',
                    'gz_sim.launch.py'
                ])
            ),
            launch_arguments={
                'gz_args': [world_path], 
                'on_exit_shutdown': 'True'
            }.items()
        )

    robot = Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'simple_robot',
                '-file', robot_file,
                '-x', '0.0',
                '-y', '0.0',
                '-z', '0.1'
            ],
            output='screen'
        )

    #TODO Update this
    bridge = RosGzBridge(
        bridge_name=LaunchConfiguration("bridge"),
        config_file=LaunchConfiguration("config_file")
    )

    return LaunchDescription([
        # Include Gazebo Sim launcher
        gz_sim,

        #Publish joint state of robot
        joint_state_publisher_gui,

        # Spawn robot
        robot
    ])