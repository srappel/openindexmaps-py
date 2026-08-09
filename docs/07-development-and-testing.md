# Chapter 7: Development and Testing

## Test Coverage Present in the Repository

The repository includes tests for core model behavior, CLI behavior, and metadata behavior.

### Core Model Tests

[`tests/test_openindexmap.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_openindexmap.py) checks:

- the default empty `OpenIndexMap`
- the default fields on `Sheet`
- schema validation of a fixture collection

### CLI Tests

[`tests/test_oimpycli.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_oimpycli.py) checks:

- `query`
- schema validation in `query`
- `map`
- schema validation failure paths
- `merge`

### Metadata Tests

[`tests/test_metadata.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_metadata.py) checks:

- default metadata values
- valid attribute setting
- invalid attribute rejection
- validation calls
- metadata file generation

## Development Signals from the Repository

The repository README says the project uses Black formatting. The repository also includes:

- fixture data under [`tests/fixture/`](/Users/srappel/Documents/github/openindexmaps-py/tests/fixture)
- notebook-based experimentation under [`notebooks/`](/Users/srappel/Documents/github/openindexmaps-py/notebooks)
- a task list in [`README.md`](/Users/srappel/Documents/github/openindexmaps-py/README.md) marking several features as still in progress

Taken together, that suggests the project is under active development and uses tests plus fixtures to pin down current behavior.

## Areas Not Confirmed by Tests

- Geodex conversion paths
- antimeridian edge cases
- `compute_details_from_oim()` metadata derivation
- the experimental code in [`extent.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/extent.py)
