from setuptools import setup, find_packages

setup(
    name="kgtoolkit",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "kgtoolkit = cli:main",
        ],
    },
)