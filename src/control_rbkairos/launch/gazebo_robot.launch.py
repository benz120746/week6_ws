#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import TimerAction, ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():
    # === Environment setup ===
    env = os.environ.copy()
    ros_lib_path = '/opt/ros/jazzy/lib'
    env['LIBGL_ALWAYS_SOFTWARE'] = '1'
    env['GZ_RENDER_ENGINE'] = 'ogre2'
    env['GZ_SIM_SYSTEM_PLUGIN_PATH'] = f"{ros_lib_path}:{env.get('GZ_SIM_SYSTEM_PLUGIN_PATH', '')}"
    env['LD_LIBRARY_PATH'] = f"{ros_lib_path}:{env.get('LD_LIBRARY_PATH', '')}"
    env['IGN_GAZEBO_SYSTEM_PLUGIN_PATH'] = f"{ros_lib_path}:{env.get('IGN_GAZEBO_SYSTEM_PLUGIN_PATH', '')}"
    env['AMENT_PREFIX_PATH'] = f"/opt/ros/jazzy:{env.get('AMENT_PREFIX_PATH', '')}"

    # === Paths ===
    world_file_path = '/home/khotkangplue_p/table.world'
    urdf_file_path = '/home/khotkangplue_p/rbkairos.urdf'

    # === 1) Start Gazebo ===
    start_gazebo_cmd = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_file_path],
        env=env,
        output='screen'
    )

    # === 2) Spawn robot ===
    spawn_robot_model = TimerAction(
        period=5.0,
        actions=[Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-file', urdf_file_path,
                '-name', 'test_robot',
                '-x', '0.0', '-y', '0.0', '-z', '0.1',
                '-world', 'table'
            ],
            parameters=[{'use_sim_time': True}],
            output='screen'
        )]
    )

    # === 3) Robot State Publisher ===
    with open(urdf_file_path, 'r') as f:
        robot_description_content = f.read()

    robot_state_publisher = TimerAction(
        period=6.0,
        actions=[Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                {'robot_description': robot_description_content},
                {'use_sim_time': True}
            ],
            output='screen'
        )]
    )

    # === 4) Bridges ===
    # (A) Clock bridge
    clock_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='clock_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '--ros-args', '-p', 'use_sim_time:=true'
        ],
        output='screen'
    )

    laser_gz_topic = '/world/default/model/test_robot/link/front_laser_link/sensor/front_laser/scan'
    
    laser_bridge_node = TimerAction(
        period=7.0,
        actions=[Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='laser_bridge',
            arguments=[
                # 👉 ปรับให้ตรงกับชื่อจริงของท็อปิกใน GZ หลัง spawn
                '/world/default/model/test_robot/link/front_laser_link/sensor/front_laser/scan'
                '@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
                '--ros-args', '-r',
                '/world/default/model/test_robot/link/front_laser_link/sensor/front_laser/scan:=/scan'
            ],
            output='screen'
        )]
    )

    # (C) TF bridge
    tf_bridge = TimerAction(
        period=7.0,
        actions=[Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='tf_bridge',
            arguments=[
                '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V]',
                '/tf_static@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V]'
            ],
            output='screen'
        )]
    )

    # === 5) Controllers ===
    joint_state_broadcaster = TimerAction(
        period=8.0,
        actions=[Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
            output='screen'
        )]
    )

    mecanum_controller = TimerAction(
        period=10.0,
        actions=[Node(
            package='controller_manager',
            executable='spawner',
            name='mecanum_drive_controller',
            arguments=['mecanum_drive_controller', '--controller-manager', '/controller_manager'],
            output='screen'
        )]
    )

    return LaunchDescription([
        start_gazebo_cmd,
        spawn_robot_model,
        robot_state_publisher,
        clock_bridge_node,
        laser_bridge_node,
        tf_bridge,
        joint_state_broadcaster,
        mecanum_controller,
    ])
