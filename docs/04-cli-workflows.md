# Chapter 4: CLI Workflows

## Current CLI Surface

The command-line interface is implemented in [`oimpycli.py`](/Users/srappel/Documents/github/openindexmaps-py/src/openindexmaps_py/oimpycli.py) using Click. The current command group exposes three commands:

- `query`
- `map`
- `merge`

There are no other CLI commands in the code reviewed.

## `query`

The `query` command reads a JSON file and either:

- prints the file back out as formatted JSON, or
- filters features by one property key and one value

When filtering is requested, it creates new `Sheet` objects from matching feature properties and wraps them in a new `OpenIndexMap`.

It also optionally validates the original loaded content against a supplied schema file.

Supported options in code are:

- `--indent` / `-i`
- `--aquery` / `-q`
- `--schema` / `-s`
- `--print-to-file` / `-f`
- `--quiet`

The CLI tests in [`tests/test_oimpycli.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_oimpycli.py) confirm query behavior with and without schemas.

## `map`

The `map` command loads a JSON file, optionally validates it against a schema, and passes it to `mapping.create_map()`. On success it prints:

`Map created at html/index.html`

The implementation does not itself open a browser. It only creates the map output.

## `merge`

The `merge` command accepts multiple input files, reads each file's `features`, adds a `note` property indicating the source filename, reconstructs each feature as a `Sheet`, and returns a merged `OpenIndexMap`.

It supports:

- `--print-to-file` / `-f`
- `--quiet`

The merge behavior is also covered by [`tests/test_oimpycli.py`](/Users/srappel/Documents/github/openindexmaps-py/tests/test_oimpycli.py).

## What the CLI Does Not Yet Show

The README mentions several CLI goals that are not represented by implemented commands:

- creating new OpenIndexMaps from scratch
- editing existing records
- reconciling or diffing two collections

Those should be treated as goals, not current CLI features.

## Follow-Up Items

There are a few details worth confirming or improving later:

- there is no console-script packaging entry point in the files reviewed
- `query` validates the original input content, not the filtered output content
- the docstring for `map` says it will open a browser, but the current command only writes output and echoes a path
