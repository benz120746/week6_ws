# robot
1. Clone โปรเจกต์จาก GitHub


2. เข้าไปในโฟลเดอร์โปรเจกต์:
cd week6_ws

3. Build workspace
colcon build --symlink-install

4.หลังจาก build เสร็จ ให้ source environment:
source install/setup.bash
source /opt/ros/jazzy/setup.bash

5.ติดตั้งปลั๊กอินฝั่ง Jazzy
sudo apt update
sudo apt install -y ros-jazzy-sdformat-urdf

6.ถ้ามันยังติด kilted อยู่ให้ลบออก
sudo apt remove -y ros-kilted-sdformat-urdf

7.โหลด env ให้สะอาด แล้วตั้งค่าให้ใช้ของ Jazzy
-ปิดโปรเซสที่อาจค้าง
pkill -f "gz sim" || true
pkill -f "parameter_bridge" || true

-เคลียร์ตัวแปรที่อาจชี้ไป distro อื่น
unset AMENT_PREFIX_PATH CMAKE_PREFIX_PATH COLCON_PREFIX_PATH LD_LIBRARY_PATH PYTHONPATH \
      GZ_CONFIG_PATH GZ_SIM_RESOURCE_PATH GZ_SIM_SYSTEM_PLUGIN_PATH

-โหลดเฉพาะ Jazzy (และ overlay ของเรา ถ้ามี)
source /opt/ros/jazzy/setup.bash
source ~/week6_ws/install/setup.bash

-บอก gz ให้มองปลั๊กอินจาก Jazzy เท่านั้น
export GZ_SIM_SYSTEM_PLUGIN_PATH=/opt/ros/jazzy/lib

-เช็คว่าไม่มีคำว่า kilted ใน env แล้ว
env | egrep 'AMENT|CMAKE|LD_LIBRARY|PYTHONPATH|GZ' | grep -i kilted || echo "OK: no kilted in env"

------ Run ทดสอย ------
8.Terminal A
ros2 launch control_rbkairos gazebo_robot.launch.py

9.Terminal B
source /opt/ros/jazzy/setup.bash
source ~/week6_ws/install/setup.bash
python3 ~/week6_ws/src/control_rbkairos/scripts/robot_movement.py

