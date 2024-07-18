import sys
import os

# Ensure the package is found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Print sys.path for debugging purposes
print("sys.path:", sys.path)


def test_import_oimpy():
    try:
        from openindexmaps_py import oimpy

        assert True, "oimpy module imported successfully"
    except ImportError as e:
        assert False, f"Failed to import oimpy: {e}"
