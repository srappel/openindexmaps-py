from setuptools import setup, find_packages

setup(
    name='openindexmaps_py',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        # List your dependencies here
    ],
)