from setuptools import setup, find_packages

setup(
    name='montecarlo',
    version='1.0.0',
    url='https://github.com/rachelegrace/DS5100-2022-06-Final.git',
    author='Rachel Grace',
    author_email='rg5xm@virginia.edu',
    description='DS5100 Final Project - Montecarlo Simulator',
    packages=find_packages(),    
    install_requires=['numpy', 'pandas', 'random', 'IPython.display'],
)