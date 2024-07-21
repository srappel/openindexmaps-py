import json
import jsonschema
from pathlib import Path

SCHEMA_PATH_GBL1 = Path("schemas/geoblacklight-schema-1.0.json")
SCHEMA_PATH_AARDVARK = "schemas/geoblacklight-schema-aardvark.json"


def load_schema_file(file_path) -> str:
    with open(file_path, "r") as schema_file:
        schema_data = json.load(schema_file)
        return schema_data
        # print(json.dumps(schema_data, indent=2))


if __name__ == "__main__":
    print(json.dumps(load_schema_file(SCHEMA_PATH_AARDVARK)).__class__)
