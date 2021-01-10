from setuptools import find_packages
from setuptools import setup

package_name = 'colcon_list_packages_changed_since'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
    ],
    install_requires=['setuptools', 'pyyaml'],
    zip_safe=False,
    author='Tyler Weaver',
    author_email='tyler@picknik.ai',
    maintainer='Tyler Weaver',
    maintainer_email='tyler@picknik.ai',
    url='https://github.com/tylerjw/colcon_lint_tools',
    # download_url='https://github.com/colcon/colcon_lint_tools/releases',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD 3-Clause License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='List packages that have changed files since point in git history.',
    license='BSD 3-Clause License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'colcon_list_packages_changed_since = colcon_list_packages_changed_since.main:main',
        ],
    },
)
