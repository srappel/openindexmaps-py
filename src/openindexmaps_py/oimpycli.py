# oimpycli.py

import click
import json
import geojson
from openindexmaps_py import mapping, oimpy
import webbrowser

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
@click.option("--indent", "-i", type=int, default=2, help="Define the JSON indentation level")
@click.option("--aquery", "-q", nargs=2, type=(str, str), default=("", None), help=r"Query the file by key-value pair. e.g. label=Sheet 1")
#@click.option("--schema", "-s", type=click.Path(exists=True), help="Path to JSON schema for validation")
def print_json(file, indent, aquery):
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
        
    click.echo(content_JSON)

# map:
@cli.command()
@click.argument(
    "file",
    nargs=1,
    type=click.File(mode="r"),
)
def map(file):
    """Create a quick Folium map and open it in the browser"""
    json_data = json.load(file)
    mapping.create_map(json.dumps(json_data))
    webbrowser.open("index.html")

# TODO: diff
# TODO: merge

if __name__ == "__main__":
    cli()
   