from setuptools import setup

VERSION = "0.2.3"

setup(
    name='woodiyc',
    version=VERSION,
    description='Wodiyc: Wooden DIY CNC machine',
    author='Andreas Florath',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities"
    ],
    install_requires=[
        "flake8",
        "flask",
        "pyinotify",
        "pylint",
        "pyyaml",
        "nose",
        "nose-cov"
    ],
    entry_points={
        'console_scripts': [
            "woodiyc_generate = wodiyc.wodiyc_generate:main",
        ]
    }
)
