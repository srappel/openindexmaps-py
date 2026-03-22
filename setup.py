from setuptools import setup, find_packages

setup(
    name="openindexmaps_py",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pyproj",
        "geojson",
        "folium",
        "requests",
        "geojson_rewind",
        "jsonschema",
        "antimeridian",
        "click",
        "shapely",
        "PyYAML",
    ],
)
