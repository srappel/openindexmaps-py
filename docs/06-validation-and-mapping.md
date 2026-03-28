# Chapter 6: Validation and Mapping

## Validation Layers

The codebase validates data at more than one level.

### GeoJSON and JSON Schema Validation

`OpenIndexMap.is_valid()` in [`oimpy.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpy.py) first checks whether the feature collection is valid according to the parent `geojson.FeatureCollection` behavior. If that passes, it validates the collection against a packaged default JSON Schema, [`src/openindexmaps_py/schemas/1.0.0.schema.json`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/schemas/1.0.0.schema.json), unless an explicit schema path is provided.

The CLI commands `query` and `map` also allow a schema file to be provided at runtime.

The test in [`tests/test_openindexmap.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_openindexmap.py) verifies a schema-validation path for an example collection.

### Geometry Normalization

The code also applies geometry-related cleanup in two places:

- `Sheet` optionally passes geometry through `antimeridian.fix_geojson()`
- string output for sheets and collections is passed through `geojson-rewind`

Those features match explicit project goals listed in the README.

## Mapping

The mapping helper in [`mapping.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/mapping.py) creates a Folium map and writes it to `html/index.html`.

The current implementation:

- creates a map using the `cartodb positron` tileset
- loads GeoJSON into a `folium.GeoJson` layer
- styles features based on the `available` property
- adds tooltips using `label` and `datePub`
- fits the map to feature bounds
- adds layer control, mouse position, and a minimap

The CLI `map` command calls this helper and reports the output path.

## Follow-Up Items

Some validation and mapping claims need to stay narrow based on the code reviewed:

- antimeridian handling is directly implemented, but I did not find separate explicit polar-validation logic
- the CLI docstring for `map` says it opens a browser, but the code path used by the CLI only creates the file and prints its location
- the module-level `main()` function in [`mapping.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/mapping.py) does fetch remote data and open a browser, but that is separate from the CLI workflow
