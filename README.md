# openindexmaps-py
A python package for OpenIndexMaps

Messing around with the geojson package.

This package uses [Black]([Black](https://black.readthedocs.io))
code style.
Black is a PEP 8 compliant opinionated formatter with its own style.

## Task List
- [x] Implement geojson-rewind
- [ ] Support for anti-meridian cutting
- [ ] Support for inset maps and extensions
- [ ] Feature Collections
- [ ] Support for CSV input
- [ ] Package and list on PyPI
- [ ] Expand the mapping functions based on folium

## Relevant Links:

### Packages
* [geojson](https://pypi.org/project/geojson/)
* [geojson-rewind](https://pypi.org/project/geojson-rewind/)
* [folium docs](https://python-visualization.github.io/folium/latest/user_guide.html)

### Related Projects
* [OpenIndexMaps](https://openindexmaps.org/)

## Known Issues
* A polygon constructed using the right hand rule crossing the
anti-meridian (180 degrees longitude) will instead render a 
polygon which wraps around the world.  
    - The GeoJSON spec says it should be represented as two polygons
    in a multipolygon
    - Just another reason to force the Right Hand Rule

    test
