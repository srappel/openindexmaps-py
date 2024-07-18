# openindexmaps-py
A python package for OpenIndexMaps

Messing around with the geojson package.

This package uses [Black]([Black](https://black.readthedocs.io))
code style.
Black is a PEP 8 compliant opinionated formatter with its own style.

## Task List
- [x] Implement geojson-rewind
- [x] Support for anti-meridian cutting
- [ ] Support for CSV input
- [ ] Package and list on PyPI
- [ ] Expand the mapping functions based on folium
- [x] JSON Schema validation

## Relevant Links:

### Packages
* [geojson](https://pypi.org/project/geojson/)
* [geojson-rewind](https://pypi.org/project/geojson-rewind/)
* [folium docs](https://python-visualization.github.io/folium/latest/user_guide.html)

### Related Projects
* [OpenIndexMaps](https://openindexmaps.org/)

## Known Issues
* ~~A polygon constructed using the right hand rule crossing the
anti-meridian (180 degrees longitude) will instead render a 
polygon which wraps around the world.~~

# Brainstorming:

* Read a shapefile? Or are we expecting table input only?
* probably need to do some date/datetype parsing in geodex.py
* Most often, people will be modifying existing OIMs, not necessarily generating new ones from scratch.
    * Tools for modifying an existing OIM, looping over records based on a query, etc.
    * Validating an existing OIM against the JSON Schema
    * Reconciling OIM against eachother:
        * Looking for records that appear on both vs one or the other
        * Generate a union list of two or more OIM
* Command line interface? Quickly entering new records from a stack of maps? Rapid cataloging

The old geodex had a really interesting way to enter records:

```dos
>p1984>e2nd>r1980
```
Which would translate to:

* Publication Year: 1984
* 2nd edition
* Photorevised 1980

Or similiar. Could it be faster than entering a form? Maybe it would be easy to include a simple form GUI? The most common fields could be their own text boxes and less common fields could be added as needed. 

Global and set-level default values, config files? yaml?

Need to consider how to handle multi-valued fields. Locaiton, for example, is an array of strings. 

* Spatial queries of index maps.
    * Point query
    * Polygon Query



