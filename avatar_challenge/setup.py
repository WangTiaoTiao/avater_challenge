from setuptools import setup
import os
from glob import glob

package_name = 'avatar_challenge'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),

        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),

        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wei',
    maintainer_email=' ',
    description='Avatar challenge robot planner',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'shape_loader = avatar_challenge.shapes_loader:main'
        ],
    },
)