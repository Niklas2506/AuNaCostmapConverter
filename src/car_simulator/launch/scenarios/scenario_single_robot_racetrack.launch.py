#!/usr/bin/env python3
#
# Copyright 2019 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Joep Tool

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument,IncludeLaunchDescription,OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_context import LaunchContext

def include_launch_description(context: LaunchContext):

    # Launch Argument Configurations
    namespace = LaunchConfiguration('namespace')
    
    # Configures the tf tree frames to include the namespace at the beginning, if the robot has a namespace
    urdf_namespace = [str(context.launch_configurations['namespace'])+'/', ''][str(context.launch_configurations['namespace']) == '']
    
    remapping_tf = [
        ('/tf', 'tf'),
        ('/tf_static', 'tf_static')
    ]
    
    # Nodes and other launch files
    costmap_to_polygon = Node(
    	package='costmap_converter',
    	executable='/home/niklas/AuNa/install/costmap_converter/bin/standalone_converter',
    	name='standalone_converter',
    	namespace=namespace,
    	remappings=remapping_tf
    )

    # Create launch description actions
    launch_description_content = []
    launch_description_content.append(costmap_to_polygon)

    return launch_description_content


def generate_launch_description():

    # Package Directories
    pkg_dir = get_package_share_directory('car_simulator')

    # Paths to folders and files
    gazebo_launch_file_dir = os.path.join(pkg_dir, 'launch', 'gazebo')
    nav_launch_file_dir = os.path.join(pkg_dir, 'launch', 'navigation')
    spawn_launch_file_dir = os.path.join(pkg_dir, 'launch', 'spawn')

    # Launch Argument Configurations
    world_name = LaunchConfiguration('world_name', default='racetrack_decorated')

    # Launch Arguments
    world_name_arg = DeclareLaunchArgument(
        'world_name',
        default_value='racetrack_decorated',
        description='Gazebo world file name'
    )
    
    # Nodes and other launch files
    world_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_launch_file_dir, 'gazebo_world.launch.py')),
        launch_arguments={
            'world_name': world_name
        }.items(),
    )
    spawn_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(spawn_launch_file_dir, 'spawn_single_robot.launch.py')),
        launch_arguments={
            'world_name': world_name
        }.items(),
    )
    nav_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav_launch_file_dir, 'navigation_single_robot.launch.py')),
        launch_arguments={
            'world_name': world_name
        }.items(),
    )
    
    # Launch Description
    ld = LaunchDescription()

    ld.add_action(world_name_arg)
    
    ld.add_action(world_cmd)
    ld.add_action(spawn_cmd)
    
    ld.add_action(nav_cmd)
    ld.add_action(OpaqueFunction(function=include_launch_description))

    return ld
