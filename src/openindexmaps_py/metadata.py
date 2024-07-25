# metadata.py

import json
from jsonschema import validate, ValidationError
from openindexmaps_py.oimpy import OpenIndexMap
from datetime import datetime, timezone

# SCHEMA_PATH_GBL1 = "schemas/geoblacklight-schema-1.0.json"
SCHEMA_PATH_AARDVARK = "schemas/geoblacklight-schema-aardvark.json"


class GeoBlacklight_Metadata:
    """
    A class to handle GeoBlacklight metadata creation, validation, and file generation
    using the defined schema.

    Attributes:
        schema (dict): The JSON schema loaded from the schema file.
        metadata (dict): The metadata to be validated and generated.
    """

    def __init__(self, metadata=None):
        """Initializes the GeoBlacklight_Metadata class with default or provided metadata."""
        self.schema = self.load_schema()
        self.metadata = metadata if metadata else self.default_metadata()

    @classmethod
    def from_file(cls, file_path: str):
        """Creates an instance of GeoBlacklight_Metadata from a JSON file."""
        metadata = None
        with open(file_path, "r") as file:
            metadata = json.load(file)
            assert isinstance(metadata, dict)
        return cls(metadata)

    def compute_details_from_oim(self, oim: OpenIndexMap):
        """Uses an OpenIndexMaps GeoJSON file to calculate an ordered set of index years and a bbox geometry for the whole file"""
        assert isinstance(oim, OpenIndexMap)

        def get_index_years(oim: OpenIndexMap) -> list[int]:
            index_years = set()
            for sheet in oim.get("features", []):
                try:
                    date_pub = sheet.get("properties", {}).get("datePub")
                    if date_pub is not None:
                        index_years.add(int(date_pub))
                except ValueError:
                    print(
                        f"Invalid datePub value: {sheet.get('properties', {}).get('datePub')}"
                    )
            return sorted(index_years)

        def get_locn_geometry(oim: OpenIndexMap) -> str:
            west, south, east, north = oim.compute_bbox()
            return f"ENVELOPE({west},{east},{north},{south})"

        index_years = get_index_years(oim)
        if index_years:
            self.set_attribute("gbl_indexYear_im", index_years)

        self.set_attribute("locn_geometry", get_locn_geometry(oim))
        self.timestamp()

    def load_schema(self):
        """Loads the JSON schema from the specified schema file."""
        with open(SCHEMA_PATH_AARDVARK, "r") as schema_file:
            return json.load(schema_file)

    def default_metadata(self):
        """Provides a default metadata structure based on the required fields."""
        return {
            "id": "",
            "dct_title_s": "",
            "gbl_resourceClass_sm": [],
            "dct_accessRights_s": "",
            "gbl_mdVersion_s": "Aardvark",
        }

    def validate_metadata(self):
        """Validates the current metadata against the JSON schema."""
        try:
            validate(instance=self.metadata, schema=self.schema)
            print("Metadata is valid.")
        except ValidationError as e:
            print(f"Metadata validation error: {e.message}")

    def set_attribute(self, attribute, value):
        """Sets an attribute in the metadata if it is valid according to the schema."""
        if attribute in self.schema["properties"]:
            self.metadata[attribute] = value
        else:
            raise KeyError(
                f"Attribute {attribute} is not valid according to the schema."
            )

    def set_references(self, oim_url: str):
        references = {
            "https://openindexmaps.org/": oim_url,
            "http://schema.org/downloadUrl/": oim_url,
        }
        json_refs = json.dumps(references, separators=(',', ':'))
        self.set_attribute("dct_references_s", json_refs)
        self.timestamp()

    def generate_metadata_file(self, filename):
        """Validates and generates the metadata file in JSON format."""
        self.validate_metadata()
        with open(filename, "w") as file:
            json.dump(self.metadata, file, indent=2)

    def timestamp(self):
        current_datetime = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.set_attribute("gbl_mdModified_dt", current_datetime)


if __name__ == "__main__":
    metadata = GeoBlacklight_Metadata()
    metadata.set_attribute("id", "12345")
    metadata.set_attribute("dct_title_s", "Example Title")
    metadata.set_attribute("gbl_resourceClass_sm", ["Datasets"])
    metadata.set_attribute("dct_accessRights_s", "Public")
    metadata.generate_metadata_file("tests/fixture/geoblacklight.json")
