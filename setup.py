from setuptools import find_packages, setup

setup(
    name="package_name",
    packages=find_packages(),
    version="1.0.0",
    description="package description",
    author="Author Name",
    author_email="autor@email.com",
    license="License",
    python_requires=">=3.9",
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
        ],
    },
)
