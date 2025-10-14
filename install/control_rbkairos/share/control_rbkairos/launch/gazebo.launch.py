#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import TimerAction, ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    
    # === Environment setup for Gazebo plugins ===
    env = os.environ.copy()
    ros_lib_path = '/opt/ros/kilted/lib'
    env['LIBGL_ALWAYS_SOFTWARE'] = '1'
    env['GZ_SIM_SYSTEM_PLUGIN_PATH'] = f"{ros_lib_path}:{env.get('GZ_SIM_SYSTEM_PLUGIN_PATH', '')}"
    env['LD_LIBRARY_PATH'] = f"{ros_lib_path}:{env.get('LD_LIBRARY_PATH', '')}"
    env['IGN_GAZEBO_SYSTEM_PLUGIN_PATH'] = f"{ros_lib_path}:{env.get('IGN_GAZEBO_SYSTEM_PLUGIN_PATH', '')}"
    env['AMENT_PREFIX_PATH'] = f"/opt/ros/kilted:{env.get('AMENT_PREFIX_PATH', '')}"
    
    
    # === Start Gazebo simulation ===
    start_gazebo_cmd = ExecuteProcess(
        cmd    = ['gz', 'sim'],
        env    = env,
        output = 'screen'
    )
    
    # === Launch Description ===
    return LaunchDescription([
        start_gazebo_cmd,
    ])