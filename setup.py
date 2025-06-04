from setuptools import setup, find_packages
import os

# Get the directory where this setup.py is located
HERE = os.path.abspath(os.path.dirname(__file__))

# Read the contents of the README.md file
try:
    with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

# List dependencies
install_requires = []

setup(
    name='quietmap',
    version='0.1.0',
    description='Quietmap – OSINT multitool for domain-based reconnaissance',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AustinSAdams/QuietMap',
    author='Austin Adams',
    license='MIT',
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Security',
            'Topic :: System :: Networking',
            'License :: OSI Approved :: MIT License',
    ],
    keywords='quietmap, nmap, network, security, scanning, discovery, automation',
    packages=find_packages(exclude=['tests', 'docs', 'build']),
    python_requires='>=3.7',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'quietmap=quietmap.__main__:main'
        ]
    },
)
