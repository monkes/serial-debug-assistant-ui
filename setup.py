#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug Assistant Setup Configuration
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='debug-assistant',
    version='1.0.0',
    author='Debug Assistant Team',
    author_email='support@debugassistant.com',
    description='A debug tool with plugin support',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/debugassistant/debug-assistant',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Debuggers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[
        'PyQt5>=5.15.0',
        'PyQt5-Qt5>=5.15.0',
        'PyQt5-sip>=12.8.0',
        'pyqt5-tools>=5.15.0',
        'PySerial>=3.5',
        'pyqt5-qt5serialport>=5.15.0',
    ],
    entry_points={
        'console_scripts': [
            'debug-assistant=debug_assistant.main:main',
        ],
    },
)
