# Chapter 5: Data Conversion and Metadata

## Geodex Support

The repository includes Geodex-related conversion code in [`geodex.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/geodex.py).

### `GeodexDictionary`

`GeodexDictionary` stores lookup tables for coded values, including:

- map type
- production
- projection
- prime meridian
- iso type
- year type

Its `lookup()` method returns the mapped string value or `None`.

### `GeodexSheet`

`GeodexSheet` reads properties from a GeoJSON feature exported from Geodex-like data. It extracts:

- record and location fields
- date and year fields
- coordinate bounds
- scale
- production
- holding status
- catalog location
- publisher
- projection
- prime meridian
- edition and iso values

Its helper methods:

- `get_dates()`: groups year values into `datePub`, `date`, `dateSurvey`, and `datePhoto`
- `get_iso()`: converts iso type and interval values into contour or bathymetric fields
- `to_sheet()`: converts the Geodex record into an `oimpy.MapSheet`

### `GeodexGeoJSON`

`GeodexGeoJSON` parses a GeoJSON feature collection from disk into `GeodexSheet` objects and can convert them into an `OpenIndexMap` with `to_openindexmap()`.

That conversion path is present in code, although it is not covered by the current tests reviewed.

## Metadata Support

The repository includes metadata generation code in [`metadata.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/metadata.py).

### `GeoBlacklight_Metadata`

`GeoBlacklight_Metadata` loads the Aardvark schema from [`schemas/geoblacklight-schema-aardvark.json`](/Users/srappel/Documents/github/openindexmaps-py/schemas/geoblacklight-schema-aardvark.json) and manages a metadata dictionary.

The default metadata includes:

- `id`
- `dct_title_s`
- `gbl_resourceClass_sm`
- `dct_accessRights_s`
- `gbl_mdVersion_s`

The class also provides methods to:

- load metadata from a file
- validate metadata against the schema
- set attributes if they are present in the schema
- set a `dct_references_s` JSON string
- write metadata to disk
- timestamp the record

### Deriving Metadata from an `OpenIndexMap`

`compute_details_from_oim()` derives:

- `gbl_indexYear_im` from `datePub` values found in the collection
- `locn_geometry` from `OpenIndexMap.compute_bbox()`
- `gbl_mdModified_dt` via `timestamp()`

This is the clearest implemented bridge between collection geometry and discovery metadata in the repository.

## Follow-Up Items

A few conversion and metadata details are not fully settled from the code alone:

- Geodex conversion is present in code but not covered by the tests reviewed
- `to_openindexmap()` in [`geodex.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/geodex.py) relies on `schema_path` that is only defined in the module's `__main__` block, so its validation path may need cleanup
- the README mentions shapefile input, but I did not find an implemented shapefile conversion module
