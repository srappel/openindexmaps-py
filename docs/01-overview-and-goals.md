# Chapter 1: Overview and Goals

## What This Repository Is

`openindexmaps-py` is a Python package for working with OpenIndexMaps data.

- Python classes for representing sheets and OpenIndexMap feature collections
- a command-line interface for querying, mapping, and merging JSON files
- JSON Schema validation for OpenIndexMap-like data
- helpers for generating GeoBlacklight/Aardvark metadata
- conversion code for Geodex-style source data
- a simple Folium-based map output

Those capabilities are visible in the source files under [`src/openindexmaps_py/`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py).

The implemented package is organized around a small number of concrete modules:

- [`oimpy.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpy.py): core `Sheet`, `MapSheet`, `PhotoFrame`, and `OpenIndexMap` classes
- [`oimpycli.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpycli.py): the current CLI commands
- [`metadata.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/metadata.py): GeoBlacklight/Aardvark metadata support
- [`geodex.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/geodex.py): Geodex lookups and conversion helpers
- [`mapping.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/mapping.py): quick HTML map generation

## The Primary Data Model

The central unit in the codebase is a `Sheet`, implemented as a subclass of `geojson.Feature`. A sheet's geometry is generated from bounding coordinates:

- `west`
- `east`
- `south`
- `north`

Those sheets can be collected into an `OpenIndexMap`, implemented as a subclass of `geojson.FeatureCollection`.

This means the current implementation is oriented toward rectangular sheet footprints described by metadata fields, not toward arbitrary geometry editing tools.

## What You Can Do with the Current Code

Based on the existing modules and tests, the repository currently supports these workflows:

- construct `Sheet` and `OpenIndexMap` objects in Python
- load an `OpenIndexMap` from a GeoJSON-like file
- validate an `OpenIndexMap` against GeoJSON rules and a JSON Schema
- query a file's features by a property key and value through the CLI
- merge multiple input files into one output collection
- build a quick Folium map from an input file
- generate GeoBlacklight/Aardvark metadata and write it to JSON
- convert Geodex-exported GeoJSON records into `MapSheet` objects and then into an `OpenIndexMap`

These are all directly represented in source files or tests in this repository.

## Project Goals

The top-level [`README.md`](/Users/srappel/Documents/github/openindexmaps-py/README.md) lists the following goals:

- create OpenIndexMaps from other formats, like Geodex or shapefiles
- edit existing OpenIndexMaps by adding or modifying records in the CLI
- create new OpenIndexMaps with the CLI
- reconcile or compare two OpenIndexMaps
- validate geometries, including antimeridian and polar coverage concerns
- enforce best practices like the right-hand rule
- validate against JSON Schema files
- make quick web maps with OpenIndexMaps

Some of those goals are already reflected in code. Others are only partially implemented or still aspirational.

## What's Implemented Now

The codebase clearly shows these implemented areas:

- JSON Schema validation
- right-hand-rule normalization via `geojson-rewind`
- antimeridian handling through the `antimeridian` package
- quick web map output through Folium
- a basic CLI with `query`, `map`, and `merge`
- metadata generation against the GeoBlacklight Aardvark schema
- Geodex conversion helpers

The test suite also exercises the default data model, schema validation, CLI commands, and metadata generation.

## What Needs Follow-Up

The repository also contains goals or hints that are not fully confirmed as complete features from the code alone:

- shapefile input support is suggested in the README, but there is not a completed shapefile ingestion workflow
- CSV input is not yet supported
- CLI-based creation or editing of new records is described as a goal, but the current CLI only exposes `query`, `map`, and `merge`
- reconcile or diff workflows are not started
- polar coverage validation in addition to antimeridian
- the package import and API surface are still fairly low-level and do not expose a polished top-level interface in [`__init__.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/__init__.py)
