# test_oimpycli.py

import json
import pytest
from click.testing import CliRunner
from openindexmaps_py.oimpycli import cli


@pytest.fixture
def sample_oim_file(tmp_path):
    """Fixture for creating a sample OpenIndexMap file"""
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "label": "46-2",
                    "name": "Test Sheet",
                    "datePub": "2024-01-01",
                    "available": True,
                },
                "geometry": {"type": "Point", "coordinates": [0, 0]},
            }
        ],
    }
    file_path = tmp_path / "sample_oim.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    return str(file_path)


@pytest.fixture
def sample_schema_file(tmp_path):
    """Fixture for creating a sample JSON Schema file"""
    schema = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "features": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "properties": {"type": "object"},
                        "geometry": {"type": "object"},
                    },
                    "required": ["type", "properties", "geometry"],
                },
            },
        },
        "required": ["type", "features"],
    }
    file_path = tmp_path / "sample_schema.json"
    with open(file_path, "w") as f:
        json.dump(schema, f)
    return str(file_path)


def test_query_command(sample_oim_file):
    runner = CliRunner()
    result = runner.invoke(
        cli, ["query", sample_oim_file, "-q", "label", "46-2", "-i", 2]
    )
    assert result.exit_code == 0
    assert '"label": "46-2"' in result.output
    assert '"name": "Test Sheet"' in result.output


def test_query_with_schema(sample_oim_file, sample_schema_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["query", sample_oim_file, "-s", sample_schema_file])
    assert result.exit_code == 0
    assert "Validation error" not in result.output


def test_query_invalid_schema(sample_oim_file, tmp_path):
    invalid_schema = {
        "type": "object",
        "properties": {"invalid_property": {"type": "string"}},
        "required": ["invalid_property"],
    }
    schema_path = tmp_path / "invalid_schema.json"
    with open(schema_path, "w") as f:
        json.dump(invalid_schema, f)

    runner = CliRunner()
    result = runner.invoke(cli, ["query", sample_oim_file, "-s", str(schema_path)])
    assert result.exit_code != 0 or "Validation error" in result.output


def test_map_command(sample_oim_file, sample_schema_file):
    runner = CliRunner()
    result = runner.invoke(cli, ["map", sample_oim_file, "-s", sample_schema_file])
    assert result.exit_code == 0
    assert "Map created" in result.output


def test_map_invalid_schema(sample_oim_file, tmp_path):
    invalid_schema = {
        "type": "object",
        "properties": {"invalid_property": {"type": "string"}},
        "required": ["invalid_property"],
    }
    schema_path = tmp_path / "invalid_schema.json"
    with open(schema_path, "w") as f:
        json.dump(invalid_schema, f)

    runner = CliRunner()
    result = runner.invoke(cli, ["map", sample_oim_file, "-s", str(schema_path)])
    assert result.exit_code != 0 or "Validation error" in result.output


def test_merge_command(sample_oim_file, tmp_path):
    runner = CliRunner()
    additional_oim_file = tmp_path / "additional_oim.json"
    additional_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "label": "46-3",
                    "name": "Additional Test Sheet",
                    "datePub": "2024-02-01",
                    "available": True,
                },
                "geometry": {"type": "Point", "coordinates": [1, 1]},
            }
        ],
    }
    with open(additional_oim_file, "w") as f:
        json.dump(additional_data, f)

    result = runner.invoke(cli, ["merge", sample_oim_file, str(additional_oim_file)])
    assert result.exit_code == 0
    assert '"label": "46-2"' in result.output
    assert '"label": "46-3"' in result.output
    assert '"note": "From source file' in result.output
