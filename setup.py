from setuptools import setup, find_packages

setup(
    name="lincmox_driver",
    version="1.0.0",
    description="Python library to control LincStation LEDs",
    author="Florent GAUDIN",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'smbus2'
    ],
    entry_points={}
)