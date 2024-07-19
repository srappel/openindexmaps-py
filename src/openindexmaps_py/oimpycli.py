# oimpycli.py

import click
import json
from openindexmaps_py import mapping
import webbrowser

@click.group()
def cli():
    pass

# print:
@cli.command()
@click.argument(
    "files",
    nargs=-1,
    type=click.File(mode="r"),
)
@click.option("--indent", "-i", type=int, default=4, help="Define the JSON indentation level")
def print(files, indent):
    """Print (Geo)JSON files"""
    for file in files:
        content = json.load(file)
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

if __name__ == "__main__":
    cli()
   