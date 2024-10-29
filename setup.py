from setuptools import setup, find_packages

setup(
    name="openindexmaps_py",
    version="0.1.1",
    package_dir={"": "src"},  # Points to the src directory
    packages=find_packages(where="src"),  # Looks for packages in src/
    install_requires=[
        # List your dependencies here
    ],
    include_package_data=True,  # Ensures non-code files are included
    package_data={
        'openindexmaps_py': [
            'config.yml',  # Include config.yml
            'schemas/*.json',  # Include all JSON schema files in the schemas directory
            'tests/*.py',  # Include test files
        ],
    },
)
