# metadata.py

import json
from jsonschema import validate, ValidationError

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

    def generate_metadata_file(self, filename):
        """Validates and generates the metadata file in JSON format."""
        self.validate_metadata()
        with open(filename, "w") as file:
            json.dump(self.metadata, file, indent=2)


if __name__ == "__main__":
    metadata = GeoBlacklight_Metadata()
    metadata.set_attribute("id", "12345")
    metadata.set_attribute("dct_title_s", "Example Title")
    metadata.set_attribute("gbl_resourceClass_sm", ["Datasets"])
    metadata.set_attribute("dct_accessRights_s", "Public")
    metadata.generate_metadata_file("tests/fixture/geoblacklight.json")
