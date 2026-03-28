import json
from importlib.resources import files
from pathlib import Path


PACKAGE_NAME = "openindexmaps_py"


def package_resource(*parts: str):
    resource = files(PACKAGE_NAME)
    for part in parts:
        resource = resource.joinpath(part)
    return resource


def load_package_json(*parts: str):
    with package_resource(*parts).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve_schema_resource(schema_path: str | Path | None, default_name: str):
    if schema_path is None:
        return package_resource("schemas", default_name)

    filesystem_path = Path(schema_path)
    if filesystem_path.exists() or filesystem_path.is_absolute():
        return filesystem_path

    packaged_schema = package_resource("schemas", filesystem_path.name)
    if packaged_schema.is_file():
        return packaged_schema

    return filesystem_path
