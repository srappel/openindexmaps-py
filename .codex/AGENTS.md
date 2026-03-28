# AGENTS.md

## Purpose

This file captures repo-specific working agreements for Codex and other agents operating in `openindexmaps-py`.

The project is a Python package for creating, editing, validating, comparing, and mapping OpenIndexMaps data. The current codebase already includes:

- Core GeoJSON/OpenIndexMap models in `src/openindexmaps_py/oimpy.py`
- CLI commands in `src/openindexmaps_py/oimpycli.py`
- Schema files in `src/openindexmaps_py/schemas/`
- Tests in `tests/`
- Example data and exploratory work in `tests/fixture/` and `notebooks/`

## Current Repo Shape

- Package source lives under `src/openindexmaps_py/`
- Tests live under `tests/`
- Schemas live under `src/openindexmaps_py/schemas/`
- Top-level docs include `README.md` and `WorkPlan.md`
- GitHub Actions workflows live under `.github/workflows/`
- Packaging is still `setup.py`-based, with `MANIFEST.in` now present
- Dependencies are listed in `requirements.txt`

## Working Agreements

- Preserve existing user changes. This repo may contain unrelated local edits; do not revert them unless explicitly asked.
- Treat `notebooks/` as exploratory unless the task specifically targets notebook work.
- Prefer changes in package code and tests over quick fixes in notebooks or fixture data.
- Keep edits consistent with the existing code style. The README explicitly states Black formatting.
- Run `black src tests` after Python code edits when practical, and keep formatting changes scoped to files you touched.
- When changing behavior, add or update tests in `tests/` when practical.
- Favor focused patches over broad refactors unless the task clearly calls for structural cleanup.
- Keep CLI changes aligned with the current Click-based interface in `src/openindexmaps_py/oimpycli.py`.
- Preserve fixture files in `tests/fixture/` unless a task explicitly requires changing test data.
- Preserve complex source geometries when working with `Sheet` or CLI query/merge paths; do not silently rebuild feature geometry from bbox fields unless that is the intended behavior.
- Be explicit about CRS assumptions. Geographic-only operations such as antimeridian normalization and bbox-derived metadata should not be applied to projected geometries.

## Repo-Specific Notes

### Package and runtime

- The package name in `setup.py` is `openindexmaps_py`
- Source import path is `openindexmaps_py`
- `requirements.txt` includes `geojson`, `geojson_rewind`, `antimeridian`, `jsonschema`, `folium`, `click`, `shapely`, `PyYAML`, and `pytest`
- `src/openindexmaps_py/config.yml` is loaded at runtime via `importlib.resources`
- Schema files are packaged under `src/openindexmaps_py/schemas/` and loaded at runtime via package resources
- `setup.py` enables `include_package_data`, and `MANIFEST.in` includes the packaged schema/config resources

### Testing

- Pytest is configured by `pytest.ini`
- Default test discovery is under `tests/`
- Useful default command: `pytest`
- GitHub Actions runs tests on `push`, `pull_request`, and manual dispatch via `.github/workflows/tests.yml`

### Code hotspots

- `src/openindexmaps_py/oimpy.py` contains the main `Sheet`, `MapSheet`, `PhotoFrame`, and `OpenIndexMap` classes
- `src/openindexmaps_py/oimpy.py` now distinguishes geographic vs. non-geographic feature inputs and preserves incoming feature geometry through `Sheet.from_feature(...)`
- `src/openindexmaps_py/oimpycli.py` currently exposes `query`, `map`, and `merge`, and query/merge should preserve feature geometry and collection CRS context
- `src/openindexmaps_py/config.yml` influences runtime behavior such as logging and antimeridian handling
- `src/openindexmaps_py/schemas/1.0.0.schema.json` is the packaged default schema used by `OpenIndexMap.is_valid()`
- `src/openindexmaps_py/metadata.py` computes GeoBlacklight details from OIMs and now rejects non-geographic bbox derivation
- `src/openindexmaps_py/oimsqlite.py` is present for initial SQLite storage helpers

### Project direction

Based on `README.md` and `WorkPlan.md`, near-term themes appear to be:

- CLI expansion
- SQLite-backed storage and caching
- Import/export workflows
- Validation and reconciliation workflows
- Better documentation

Agents should bias toward solutions that support those directions rather than one-off scripts, unless a one-off script is what the user asked for.

## Commands I’d Commonly Reach For

- `pytest`
- `pytest tests/test_oimpycli.py`
- `python -m openindexmaps_py.oimpycli --help`

## Open Questions To Refine Later

- Preferred Python version and environment manager are not documented yet
- There is no documented formatter/linter command yet beyond the README note about Black
- It is not yet clear whether SQLite work is experimental or part of the primary path forward

Update this file as conventions become explicit.
