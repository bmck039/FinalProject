from setuptools import setup, find_packages

setup(
    name='spades',
    version='0.1.0',
    description='Spades Gym Environment',
    packages=find_packages(),
    install_requires=[
        'gym>=0.9.4,<=0.15.7',
        'numpy>=1.13.0',        
    ]
)


