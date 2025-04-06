from setuptools import setup, find_packages

setup(
    name='llc_rules_extractor',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt5',
        'rdflib',
        'matplotlib',
        'networkx',
        'pyparsing',
    ],
    entry_points={
        'console_scripts': [
            'llc-launch=app.main:main', 
        ],
    },
)