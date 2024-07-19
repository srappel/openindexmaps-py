# openindexmaps-py

A Python package for OpenIndexMaps

## Goals:
* Create OpenIndexMaps from other formats, like Geodex or Shapefiles
* Edit existing OpenIndexMaps by adding or modifying records in the CLI
* Create new OpenIndexMaps with the CLI
* Reconcile/Compare/Diff two OpenIndexMaps from different institutions
* Validate geometries (Antimeridian cutting, polar coverage), Validate GeoJSON
* Enforce best practices like the right-hand rule
* Validate against JSON Schema files
* Make quick web maps with OpenIndexMaps

This package uses [Black](https://black.readthedocs.io) code style. Black is a PEP 8 compliant opinionated formatter with its own style.

## Task List
- [x] Implement geojson-rewind
- [x] JSON Schema validation
- [x] Support for anti-meridian cutting
- [ ] Support for CSV input
- [ ] Expand the mapping functions based on folium
- [ ] Command Line Interface
- [ ] Documentation
- [ ] Package and list on PyPI

## Dependencies
* [geojson](https://pypi.org/project/geojson/) - Since OpenIndexMaps must be valid GeoJSON, this package makes it easy to create and validate GeoJSON objects
* [geojson-rewind](https://pypi.org/project/geojson-rewind/) - Enforces the right-hand rule
* [antimeridian](https://antimeridian.readthedocs.io/en/stable/) - Fix GeoJSON geometries that cross the antimeridian and/or the poles
* [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/) - Validate (Geo)JSON against a JSON Schema file - e.g., confirm output is a valid OpenIndexMap
* [folium](https://python-visualization.github.io/folium/latest/user_guide.html) - Make quick leaflet.js maps

## Related Projects
* [OpenIndexMaps](https://openindexmaps.org/)

## Brainstorming Space:

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



