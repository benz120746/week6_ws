from setuptools import setup
from glob import glob
import os

package_name = 'control_rbkairos'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],  # โฟลเดอร์: src/control_rbkairos/control_rbkairos
    data_files=[
        # ให้ ament รู้จักแพ็กเกจ (จำเป็นสำหรับ ros2 run / ros2 launch)
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        # package.xml
        (os.path.join('share', package_name), ['package.xml']),
        # launch files (.py)
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        # urdf/xacro (มีไฟล์ไหนก็จะถูกติดตั้งไปด้วย)
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.*')),
        # (ถ้ามีโฟลเดอร์ config/ และ .yaml ให้ติดตั้งด้วย)
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ชื่อคุณ',
    maintainer_email='อีเมลคุณ',
    description='RBKairos control nodes and demos (mecanum)',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # node ภายในแพ็กเกจ control_rbkairos/
            'move_robot = control_rbkairos.move_robot:main',
            'rbkairos_distance_demo = control_rbkairos.rbkairos_mecanum_distance_demo:main',
            'rbkairos_mecanum_drive = control_rbkairos.rbkairos_mecanum_drive:main',
        ],
    },
)
