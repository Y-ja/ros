from setuptools import find_packages, setup

package_name = 'my_package'

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
    description='homw demo',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = my_package.my_node:main',
            'hello_class = my_package.hello_class:main', 
            'hello_pub = my_package.hello_pub:main',
            'hello_sub = my_package.hello_sub:main',
            'time_pub = my_package.time_pub:main', 
        ],
    },
)
