from setuptools import setup, find_packages
setup(
    name = "nightwatcher",
    version = "0.1",
    packages = find_packages(),
    install_requires = [
        'APScheduler==3.2.0',
        'libvirt-python==3.3.0',
        'lxml==3.8.0',
        'requests==2.18.1',
        'redis==2.10.5'
    ],
    entry_points = {
        'console_scripts': [
            'nightwatcher = monitor.app:main',
        ]
    }
)