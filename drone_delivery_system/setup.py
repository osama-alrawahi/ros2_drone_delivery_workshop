from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'drone_delivery_system'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Workshop Student',
    maintainer_email='student@university.edu',
    description='ROS2 Drone Delivery System Workshop',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Nodes (Part 4)
            'drone_status_node      = drone_delivery_system.drone_status_node:main',
            'battery_monitor_node   = drone_delivery_system.battery_monitor_node:main',
            'gps_node               = drone_delivery_system.gps_node:main',
            # Ground control (Part 5)
            'ground_control_node    = drone_delivery_system.ground_control_node:main',
            # Service servers/clients (Part 6)
            'takeoff_service_server     = drone_delivery_system.takeoff_service_server:main',
            'takeoff_service_client     = drone_delivery_system.takeoff_service_client:main',
            'destination_service_server = drone_delivery_system.destination_service_server:main',
            'destination_service_client = drone_delivery_system.destination_service_client:main',
            # Action server/client (Part 7)
            'delivery_action_server = drone_delivery_system.delivery_action_server:main',
            'delivery_action_client = drone_delivery_system.delivery_action_client:main',
        ],
    },
)
