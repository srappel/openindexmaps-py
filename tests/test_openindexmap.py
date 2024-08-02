import geojson
import logging
from pathlib import Path
from openindexmaps_py.oimpy import (
    OpenIndexMap,
    Sheet,
)  # Adjust the import based on your package structure

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_default_oim():
    # return {"type": "FeatureCollection", "features": []}
    defaultoim = OpenIndexMap()
    assert defaultoim.__geo_interface__["type"] == "FeatureCollection"
    assert defaultoim.__geo_interface__["features"] == []

def test_default_sheet_dict():
    sheet = Sheet()  # Assume Sheet initializes attributes with default values
    # Assert that each attribute of the Sheet object matches the expected default
    assert sheet["properties"]["label"] == "", "Label should be an empty string"
    assert sheet["properties"]["title"] == "", "Title should be an empty string"
    assert sheet["properties"]["location"] == [], "Location should be an empty list"
    assert (
        sheet["properties"]["datePub"] == ""
    ), "Date of publication should be an empty string"
    assert (
        sheet["properties"]["available"] == ""
    ), "Availability should be an empty string"
    assert sheet["properties"]["west"] == 0.0, "West should be 0.0"
    assert sheet["properties"]["east"] == 1.0, "East should be 1.0"
    assert sheet["properties"]["north"] == 1.0, "North should be 1.0"
    assert sheet["properties"]["south"] == 0.0, "South should be 0.0"


def test_openindexmap_validation():
    fixture_path = Path("tests/fixture/MillionthMap.geojson")
    assert fixture_path.exists(), "Fixture file does not exist."

    with fixture_path.open() as file:
        gj = geojson.load(file)
        features = gj["features"]

        open_index_map = OpenIndexMap(features)
        logger.info(f"\nOpenIndexMap:\n{str(open_index_map)}\n")

        schema_path = Path("schemas/1.0.0.schema.json")
        assert schema_path.exists(), "Schema file does not exist."

        print(open_index_map)

        assert open_index_map.is_valid(
            str(schema_path)
        ), "The OpenIndexMap is not valid."


if __name__ == "__main__":
    import pytest

    pytest.main()
