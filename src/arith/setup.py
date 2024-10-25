from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'arith'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob(os.path.join('launch', '*.launch.py'))),
        ('share/' + package_name + '/param', glob(os.path.join('param', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Won_JAE',  
    maintainer_email='ghkdwo34@naver.com',
    description='Arithmetic final demo',  
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'argument = arith.argument:main',
            'calculator = arith.calculator:main',
            'operarot = arith.operarot:main',
            
        ],
    },
)
