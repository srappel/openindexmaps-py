# Chapter 3: Core Data Models

## `Sheet`

The `Sheet` class in [`oimpy.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpy.py) subclasses `geojson.Feature`. It builds a polygon geometry from bounding coordinates in the input dictionary:

- `west`
- `east`
- `south`
- `north`

If no input dictionary is provided, `Sheet.default_sheet_dict()` supplies default values:

- `label`: `""`
- `title`: `""`
- `location`: `[]`
- `datePub`: `""`
- `available`: `""`
- `west`: `0.0`
- `east`: `1.0`
- `north`: `1.0`
- `south`: `0.0`

These defaults are also asserted in [`tests/test_openindexmap.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_openindexmap.py).

## Sheet Properties and Attributes

After constructing the GeoJSON feature, `Sheet` copies many fields into object attributes, including:

- labels and dates
- bounding coordinates
- location and scale
- institution and holding information
- download and web URLs
- notes

The `properties` dictionary is still the underlying GeoJSON representation, but the extra attributes make it easier to work with common fields directly.

## Geometry Handling

The geometry for a `Sheet` is always built as a rectangular polygon from its coordinate bounds. When `fix-antimeridian` is enabled in configuration, that geometry is passed through `antimeridian.fix_geojson()`.

The class also uses `geojson-rewind` when converting the object to a string.

## `MapSheet` and `PhotoFrame`

Two subclasses extend `Sheet`:

- `MapSheet`: adds fields such as alternate titles, survey and photo dates, edition, publisher, projection, contour information, bathymetric information, and prime meridian
- `PhotoFrame`: adds fields such as `photomos`, `bands`, `rectificn`, and `rollNo`

These subclasses preserve the same geometry-building behavior while expanding metadata fields for more specific use cases.

## `OpenIndexMap`

`OpenIndexMap` subclasses `geojson.FeatureCollection`. It is the collection type used throughout the repository.

Key behaviors include:

- building a feature collection from a list of `geojson.Feature` objects
- returning a GeoJSON-style `__geo_interface__`
- loading a collection from a file with `from_file()`
- adding a sheet with `add_sheet()`
- validating against GeoJSON and JSON Schema with `is_valid()`
- computing a collection bounding box with `compute_bbox()`

The default empty collection behavior is also tested in [`tests/test_openindexmap.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_openindexmap.py).

## Important Implementation Detail

`OpenIndexMap.from_file()` rebuilds sheets from each feature's `properties`, not from the original input geometry. That means the current implementation assumes the necessary bounding fields are present in the properties.

## Follow-Up Items

There are a few model-related details worth clarifying later:

- `OpenIndexMap.default_oim()` returns a dictionary, while the constructor filters for feature objects; the empty default case still works in tests, but the constructor pattern is slightly unusual
- the code imports `Path` in [`oimpy.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpy.py) without using it
- the current API surface is module-level rather than a polished top-level package API
