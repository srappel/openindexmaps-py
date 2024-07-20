# oimpycli.py

import click
import json
import geojson
from openindexmaps_py import mapping, oimpy
import webbrowser
from jsonschema import validate, ValidationError


@click.group()
def cli():
    pass


# print-json:
@cli.command()
@click.argument(
    "file",
    nargs=1,
    type=click.File(mode="r"),
)
@click.option(
    "--indent", "-i", type=int, default=2, help="Define the JSON indentation level"
)
@click.option(
    "--aquery",
    "-q",
    nargs=2,
    type=(str, str),
    default=("", None),
    help=r"Query the file by key-value pair. e.g. `-q label 46-2` to find sheets with the label name 46-2",
)
@click.option(
    "--schema",
    "-s",
    type=click.Path(exists=True),
    help="Provide a file path to a JSON Schema file and validate against it",
)
@click.option(
    "--print-to-file",
    "-f",
    type=click.Path(),
    help="Write output to (geo)json file. e.g. `-f f0303_queryResult.geojson`",
)
def print_json(file, indent, aquery, schema, print_to_file):
    """Print (Geo)JSON files"""
    content = json.load(file)
    assert isinstance(content, dict)

    # Check if there's a query
    if aquery[0] != "":
        k, v = aquery
        assert isinstance(k, str)
        click.echo(f"Query: {k}=={v} ({v.__class__})...\n")

        output_features = []
        for feature in content.get("features"):
            feature_properties = feature.get("properties")
            if str(feature_properties.get(k, "")) == v:
                feature_sheet = oimpy.Sheet(feature_properties)
                assert isinstance(feature_sheet, oimpy.Sheet)
                output_features.append(feature_sheet)

        output_OIM = oimpy.OpenIndexMap(output_features)
        content_JSON = json.dumps(output_OIM.__geo_interface__, indent=indent)
    else:
        content_JSON = json.dumps(content, indent=indent)

    if schema:
        with open(schema, "r") as schema_file:
            schema_data = json.load(schema_file)
            try:
                validate(instance=content, schema=schema_data)
            except ValidationError as e:
                click.echo(f"Validation error: {e.message}\n")
                return

    if print_to_file:
        try:
            with open(print_to_file, "w") as output_file:
                output_file.write(content_JSON)
        except Exception as e:
            click.echo(e)
            return

    click.echo(content_JSON)


# map:
@cli.command()
@click.argument(
    "file",
    nargs=1,
    type=click.File(mode="r"),
)
@click.option(
    "--schema",
    "-s",
    type=click.Path(exists=True),
    help="Path to JSON schema for validation",
)
def map(file, schema):
    """Create a quick Folium map and open it in the browser"""
    json_data = json.load(file)

    if schema:
        with open(schema, "r") as schema_file:
            schema_data = json.load(schema_file)
            try:
                validate(instance=json_data, schema=schema_data)
            except ValidationError as e:
                click.echo(f"Validation error: {e.message}\n")

    try:
        mapping.create_map(json.dumps(json_data))
    except Exception as e:
        click.echo(f"Error creating the map: {e.message}\n")


# merge
@cli.command()
@click.argument("files", nargs=-1, type=click.File(mode="r"))
@click.option(
    "--print-to-file",
    "-f",
    type=click.Path(),
    help="Write output to (geo)json file. e.g. `-f f0303_queryResult.geojson`",
)
def merge(files, print_to_file):
    """Merge multiple OpenIndexMaps into a single OpenIndexMap."""
    output_feature_sheets = []

    for file in files:
        json_data = json.load(file)
        oim_features = json_data.get("features", [])
        for feature in oim_features:
            assert isinstance(feature, dict)
            feature["properties"]["note"] = f"From source file {file.name}"
            feature_sheet = oimpy.Sheet(feature.get("properties"))
            output_feature_sheets.append(feature_sheet)

    output_oim = oimpy.OpenIndexMap(output_feature_sheets)

    content_JSON = json.dumps(output_oim.__geo_interface__, indent=4)

    if print_to_file:
        try:
            with open(print_to_file, "w") as output_file:
                output_file.write(content_JSON)
        except Exception as e:
            click.echo(e)
            return

    click.echo(content_JSON)


# TODO: diff

if __name__ == "__main__":
    cli()
