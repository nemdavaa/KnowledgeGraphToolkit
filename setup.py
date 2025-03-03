from setuptools import setup, find_packages

setup(
    name="KGToolKit",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "KGToolKit = cli:main",
        ],
    },
)