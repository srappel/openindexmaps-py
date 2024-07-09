import geojson
import logging
import json
from pathlib import Path
from openindexmaps_py.oimpy import OpenIndexMap  # Adjust the import based on your package structure

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openindexmap_validation():
    fixture_path = Path("tests/fixture/MillionthMap.geojson")
    assert fixture_path.exists(), "Fixture file does not exist."

    with fixture_path.open() as file:
        gj = geojson.load(file)
        features = gj['features']

        open_index_map = OpenIndexMap(features)
        logger.info(f"\nOpenIndexMap:\n{str(open_index_map)}\n")

        schema_path = Path("src/openindexmaps_py/1.0.0.schema.json")
        assert schema_path.exists(), "Schema file does not exist."

        print(open_index_map)

        assert open_index_map.is_valid(str(schema_path)), "The OpenIndexMap is not valid."

if __name__ == "__main__":
    import pytest
    pytest.main()