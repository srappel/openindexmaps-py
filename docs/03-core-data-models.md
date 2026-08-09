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

`Sheet` supports two geometry workflows:

- creating a new sheet from bounding fields
- rebuilding a sheet from an existing GeoJSON feature

For new sheet dictionaries, `Sheet.__init__()` calls `_geometry_from_bbox()`. This function builds a rectangular `geojson.Polygon` from `west`, `east`, `south`, and `north` in this coordinate order:

1. southwest
2. southeast
3. northeast
4. northwest
5. southwest again to close the ring

If a coordinate field is missing, `_geometry_from_bbox()` falls back to `0.0` for that coordinate. After the rectangle is built, the function checks the package configuration. When `fix-antimeridian` is enabled in [`config.yml`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/config.yml), the rectangle is passed through `antimeridian.fix_geojson()`. This allows a bounding-box sheet that crosses the antimeridian to be normalized into valid GeoJSON, usually by splitting it into a `MultiPolygon`.

For existing GeoJSON features, `Sheet.from_feature()` passes the feature into the regular constructor. The constructor detects feature-like dictionaries with `_looks_like_feature()`, copies the feature `properties`, and sends the existing `geometry` to `_normalize_feature_geometry()` instead of rebuilding it from `west`, `east`, `south`, and `north`. This preserves non-rectangular footprints such as detailed `Polygon` or `MultiPolygon` sheet outlines.

Before normalizing an existing feature geometry, the class checks whether the coordinates look geographic. `_is_spatially_geographic()` uses a declared feature CRS, a collection-level CRS passed from `OpenIndexMap.from_file()`, or coordinate ranges from `_geometry_looks_geographic()`:

- WGS84-like CRS names such as `EPSG:4326`, `CRS84`, or `WGS 84` are treated as geographic.
- Non-geographic CRS declarations are preserved but skipped for geographic normalization.
- Features without CRS metadata are treated as geographic only when all coordinate positions look like longitude and latitude values.

`_normalize_feature_geometry()` only applies `antimeridian.fix_geojson()` when the geometry is geographic, `fix-antimeridian` is enabled, and the geometry type is `Polygon` or `MultiPolygon`. Non-geographic geometries are returned unchanged, and the `Sheet` stores `spatially_geographic` and `spatial_reason` so later workflows can make safer decisions.

`OpenIndexMap.compute_bbox()` uses those flags when creating a collection-level geographic bounding box. It refuses to compute a geographic bbox for a `Sheet` marked as non-geographic, then uses Shapely's `shape(...).bounds` to accumulate `[west, south, east, north]` across the collection.

The string output path also normalizes winding order. `Sheet.__str__()` serializes the feature with `geojson.dumps(..., indent=4)` and passes the result through `geojson_rewind.rewind()`. `OpenIndexMap.__str__()` does the same for the full feature collection.

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

`OpenIndexMap.from_file()` rebuilds each feature as a `Sheet` by calling `Sheet.from_feature()`. That preserves the incoming feature geometry rather than forcing the sheet to be rebuilt from `west`, `east`, `south`, and `north` property values.

This matters for imported OpenIndexMaps that contain complex footprints, antimeridian-split `MultiPolygon` geometries, or projected geometries from a declared collection CRS. In those cases, the geometry remains attached to the feature, while the feature's `properties` are still copied into the new `Sheet`.

## Follow-Up Items

- consider simplifying `OpenIndexMap.default_oim()` or the constructor default path so the empty collection case is more explicit
- consider adding broader regression coverage around `OpenIndexMap.from_file()` preserving complex imported geometries
- consider whether the package should expose a more polished top-level API. At the moment, users need to know which module contains each class or helper, such as importing `Sheet`, `MapSheet`, and `OpenIndexMap` from `openindexmaps_py.oimpy`. A cleaner public API could re-export the main classes and conversion helpers from `openindexmaps_py.__init__`, document those imports as stable, and leave lower-level implementation modules free to change over time.
