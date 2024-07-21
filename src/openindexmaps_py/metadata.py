# metadata.py

import json
from jsonschema import validate, ValidationError

#SCHEMA_PATH_GBL1 = "schemas/geoblacklight-schema-1.0.json"
SCHEMA_PATH_AARDVARK = "schemas/geoblacklight-schema-aardvark.json"


def load_schema_file(file_path) -> str:
    with open(file_path, "r") as schema_file:
        schema_data = json.load(schema_file)
        return schema_data
        # print(json.dumps(schema_data, indent=2))


class GeoBlacklight_Metadata:
    
    def __init__(self, metadata=None):
        self.schema = self.load_schema()
        self.metadata = metadata if metadata else self.default_metadata()

    def load_schema(self):
        with open(SCHEMA_PATH_AARDVARK, 'r') as schema_file:
            return json.load(schema_file)

    def default_metadata(self):
        return {
            "id": "",
            "dct_title_s": "",
            "gbl_resourceClass_sm": [],
            "dct_accessRights_s": "",
            "gbl_mdVersion_s": "Aardvark"
        }

    def validate_metadata(self):
        try:
            validate(instance=self.metadata, schema=self.schema)
            print("Metadata is valid.")
        except ValidationError as e:
            print(f"Metadata validation error: {e.message}")

    def set_attribute(self, attribute, value):
        if attribute in self.schema['properties']:
            self.metadata[attribute] = value
        else:
            raise KeyError(f"Attribute {attribute} is not valid according to the schema.")

    def generate_metadata_file(self, filename):
        self.validate_metadata()
        with open(filename, 'w') as file:
            json.dump(self.metadata, file, indent=2)



if __name__ == "__main__":
    metadata = GeoBlacklight_Metadata()
    metadata.set_attribute('id', '12345')
    metadata.set_attribute('dct_title_s', 'Example Title')
    metadata.set_attribute('gbl_resourceClass_sm', ['Datasets'])
    metadata.set_attribute('dct_accessRights_s', 'Public')
    metadata.generate_metadata_file('tests/fixture/geoblacklight.json')
