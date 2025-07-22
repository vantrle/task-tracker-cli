from setuptools import setup, find_packages

setup(
    name="task_tracker_cli",
    version="0.1.0",
    description="A simple CLI task tracker",
    author="vantrle",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "task-cli=task_tracker.cli:main"
        ]
    },
    python_requires='>=3.6',
)
