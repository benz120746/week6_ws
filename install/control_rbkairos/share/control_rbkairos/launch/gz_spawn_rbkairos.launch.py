from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_prefix
import os

def generate_launch_description():
    robot_ns = 'robot1'

    # path ของไฟล์ xacro (อันนี้ใช้ get_package_share_directory ก็ได้ถ้าคุณมีอยู่แล้ว)
    from ament_index_python.packages import get_package_share_directory
    xacro_file = os.path.join(
        get_package_share_directory('robotnik_description'),
        'robots', 'rbkairos', 'rbkairos.urdf.xacro'
    )

    # === เพิ่มบรรทัดตั้งค่า GZ_SIM_RESOURCE_PATH ให้ชี้ไปที่ ".../share"
    shares = []
    for pkg in ['robotnik_description', 'robotnik_common', 'robotnik_sensors']:
        try:
            shares.append(os.path.join(get_package_prefix(pkg), 'share'))
        except Exception:
            pass  # บางเครื่องอาจไม่มี robotnik_sensors ก็ข้ามได้

    set_res_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=':'.join(shares + [os.environ.get('GZ_SIM_RESOURCE_PATH', '')])
    )
    # === จบส่วนเพิ่ม

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=robot_ns,
        parameters=[{'use_sim_time': True,
                     'robot_description': Command(['xacro ', xacro_file])}],
        output='screen'
    )

    gz = ExecuteProcess(cmd=['gz', 'sim', '-r', 'empty.sdf'], output='screen')

    create = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', f'/{robot_ns}/robot_description',
            '-name', 'rbkairos',
            '-x', '0', '-y', '0', '-z', '0.1'
        ],
        output='screen'
    )

    return LaunchDescription([set_res_path, rsp, gz, create])
