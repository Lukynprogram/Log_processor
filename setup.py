from setuptools import setup, find_packages

setup(
    name="log_analyzer",
    version="1.0.0",
    description="EPAM - CLI tool for analyzing log files",
    author="Lukas Jonak",
    author_email="lukas00028@protonmail.com",
    packages=find_packages(),
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'log-analyzer=log_analyzer.cli:main',
        ],
    },
    install_requires=[],
)
