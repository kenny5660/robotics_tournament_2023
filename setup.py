import os
from os.path import join, dirname
from setuptools import setup, find_packages

import robotics_tournament_2023

setup(
    name='robotics_tournament_2023',
    version=robotics_tournament_2023.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'pyserial==3.5',
        'opencv-python==4.8.1.78',
        'ultralytics==8.0.227'
    ],
    entry_points={
        'console_scripts':
            ['robotics_tournament_2023 = robotics_tournament_2023.__main__:main',
             'add_img_dataset = robotics_tournament_2023.add_img_dataset:main']
    }
)