#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import TimerAction, ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    
    # === Environment setup for Gazebo plugins ===
    env = os.environ.copy()  
    ros_lib_path = '/opt/ros/jazzy/lib'
    env['LIBGL_ALWAYS_SOFTWARE'] = '1'
    env['GZ_SIM_SYSTEM_PLUGIN_PATH'] = f"{ros_lib_path}:{env.get('GZ_SIM_SYSTEM_PLUGIN_PATH', '')}"
    env['LD_LIBRARY_PATH'] = f"{ros_lib_path}:{env.get('LD_LIBRARY_PATH', '')}"
    env['IGN_GAZEBO_SYSTEM_PLUGIN_PATH'] = f"{ros_lib_path}:{env.get('IGN_GAZEBO_SYSTEM_PLUGIN_PATH', '')}"
    env['AMENT_PREFIX_PATH'] = f"/opt/ros/kilted:{env.get('AMENT_PREFIX_PATH', '')}"
    
    world_file_path = '/home/khotkangplue_p/table.world'
    
    # === Start Gazebo simulation ===
    start_gazebo_cmd = ExecuteProcess(
        cmd    = ['gz', 'sim', '-r', world_file_path],
        env    = env,
        output = 'screen'
    )

    # === File path for the world model ===
    urdf_file_path = '/home/khotkangplue_p/rbkairos.urdf'

    # === Load robot description from URDF ===
    with open(urdf_file_path, 'r') as urdf_file:
        robot_description_content = urdf_file.read()
    robot_description_param = {'robot_description': robot_description_content}

    # === Spawn robot entity into Gazebo ===
    spawn_robot_model = TimerAction(
        period =5.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-file', urdf_file_path,
                    '-name', 'test_robot',
                    '-x', '0.0', '-y', '0.0', '-z', '0.1'
                ],
                parameters=[{'use_sim_time': True}],
                output='screen'
            )
        ]
    )

    # === Robot State Publisher ===
    robot_state_publisher = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                parameters=[
                    robot_description_param,
                    {'use_sim_time': True}
                ],
                output='screen'
            )
        ]
    )
    robot_joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen'
    )
    # === Clock bridge (GZ -> ROS 2) ===
    clock_bridge_node = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    name='clock_bridge',
    arguments=[
        '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        '--ros-args',
        '-p', 'use_sim_time:=true'
    ],
    output='screen'
)
    
    diff_drive_controller = Node(
        package='controller_manager',
        executable='spawner',
        name='diff_drive_controller',
        arguments=['diff_drive_controller', '--controller-manager', '/controller_manager'],
        output='screen'
    )

    # === Launch Description ===
    return LaunchDescription([
        start_gazebo_cmd,
        spawn_robot_model,
        robot_state_publisher,
        robot_joint_state_broadcaster,
        clock_bridge_node,
        diff_drive_controller,
    ])