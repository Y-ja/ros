from setuptools import find_packages, setup

package_name = 'simple_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='test',
    maintainer_email='ghkdwo34@naver.com',
    description='simple_ros demo',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "hello = simple_ros.hello:main",  # main 함수를 호출
            "hello_class = simple_ros.hello_class:main",  # main 함수를 호출
            "hello_sub = simple_ros.hello_sub:main",  # main 함수를 호출
            "hello_pub = simple_ros.hello_pub:main",# main 함수를 호출
            "time_pub = simple_ros.time_pub:main",# main 함수를 호출
            
        ],

    },
)
