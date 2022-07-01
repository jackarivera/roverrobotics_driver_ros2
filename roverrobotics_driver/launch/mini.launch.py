from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node


def generate_launch_description():
    # urdf = Path(get_package_share_directory(
    #     'roverrobotics_description'), 'urdf', 'rover.urdf')
    # assert urdf.is_file()
    robot_config = Path(get_package_share_directory(
        'roverrobotics_driver'), 'config', 'mini_config.yaml')
    localization_config = Path(get_package_share_directory(
        'roverrobotics_driver'), 'config', 'ekf.yaml')
    ld = LaunchDescription()

    robot_driver = Node(
        package = 'roverrobotics_driver',
        name = 'roverrobotics_driver',
        executable = 'roverrobotics_driver',
        parameters = [robot_config],
        respawn=True,
        respawn_delay=1
    )
    
    robot_localization = Node(
        package = 'robot_localization',
        name = 'ekf_filter_node',
        executable = 'ekf_node',
        parameters = [localization_config]
    )
    
    imu_node = Node(
        package = 'bno055_driver',
        name = 'bno055_driver',
        executable = 'bno055_driver'
    )

    ld.add_action(robot_driver)
    ld.add_action(robot_localization)
    ld.add_action(imu_node)

    return ld
