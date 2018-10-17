from setuptools import setup, find_packages

setup(
    name='criteo-performance-pipeline',
    version='1.0.0',
    description="A data integration pipeline that imports downloaded Criteo campaign performance data into a data warehouse",

    install_requires=[
        'criteo-performance-downloader>=1.4.1',
        'etl-tools>=1.1.0',
        'data-integration>=1.3.0'
    ],

    dependency_links=[
        'git+https://github.com/mara/criteo-performance-downloader.git@1.4.1#egg=criteo-performance-downloader-1.4.1',
        'git+https://github.com/mara/etl-tools.git@1.1.0#egg=etl-tools-1.1.0',
        'git+https://github.com/mara/data-integration.git@1.3.0#egg=data-integration-1.3.0'

    ],
    packages=find_packages(),

    author='Mara contributors',
    license='MIT'
)
