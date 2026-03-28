# Chapter 2: Installation and Project Layout

## What the Repository Contains

The project uses a `src/` layout with package code under [`src/openindexmaps_py/`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py). Other important top-level directories are:

- [`tests/`](/Users/srappel/Documents/github/openindexmaps-py/tests): unit tests and fixture-driven tests
- [`schemas/`](/Users/srappel/Documents/github/openindexmaps-py/schemas): JSON Schema files
- [`notebooks/`](/Users/srappel/Documents/github/openindexmaps-py/notebooks): notebook experiments and sample files
- [`db/`](/Users/srappel/Documents/github/openindexmaps-py/db): a SQLite database used in experimentation

This layout supports both library-style development and ad hoc experimentation.

## Installation from Source

The package has a minimal [`setup.py`](/Users/srappel/Documents/github/openindexmaps-py/setup.py) that defines the package name, version, and `src/` package directory. The code imports dependencies that are listed in [`requirements.txt`](/Users/srappel/Documents/github/openindexmaps-py/requirements.txt), including:

- `pyproj`
- `geojson`
- `folium`
- `requests`
- `geojson_rewind`
- `jsonschema`
- `antimeridian`
- `pytest`
- `click`
- `shapely`

The repository does not include fuller installation instructions beyond those files, so the safest documented assumption is a source install in a Python environment where those dependencies are available.

## Package Entry Points

The package directory contains an empty [`__init__.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/__init__.py), so the codebase does not currently present a curated top-level public API.

Instead, the implemented entry points are module-level:

- import core classes from [`oimpy.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpy.py)
- run the CLI from [`oimpycli.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpycli.py)
- use metadata helpers from [`metadata.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/metadata.py)

## Configuration

The file [`config.yml`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/config.yml) is loaded by [`oimpy.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpy.py) at import time. It currently sets:

- `fix-antimeridian`
- `logging-level`
- `sheet-validation-warn`

Because the code opens this config file using a relative path, the repository root appears to be the expected working directory when running the package directly from source.

## Files to Understand First

If you are orienting yourself in the repository, these files provide the clearest starting points:

- [`README.md`](/Users/srappel/Documents/github/openindexmaps-py/README.md): stated goals, task list, and brainstorming notes
- [`src/openindexmaps_py/oimpy.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpy.py): core data model
- [`src/openindexmaps_py/oimpycli.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpycli.py): current CLI surface
- [`tests/test_openindexmap.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_openindexmap.py): default collection and schema-validation behavior
- [`tests/test_oimpycli.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_oimpycli.py): exercised CLI workflows
- [`tests/test_metadata.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_metadata.py): exercised metadata behavior

## Follow-Up Items

The repository leaves a few installation-related details unclear:

- no Python version is specified in the files reviewed
- `setup.py` does not declare install requirements yet
- there is no documented console-script entry point for the CLI

Those are worth clarifying in the package configuration later.
