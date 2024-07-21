from setuptools import setup, find_packages

setup(
    name='pymongosh',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'prompt_toolkit>=3.0.0',
        'pymongo>=3.11.0',
        'bson>=0.5.10',
    ],
    entry_points={
        'console_scripts': [
            'pymongosh=pymongosh.main:main',
        ],
    },
    description="A CLI tool to emulate MongoDB's mongosh using prompt-toolkit",
    author='sss7526',
    author_email='',
    url='https://github.com/sss7526/pymongosh',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)