from openindexmaps_py import oimpy
import geojson
from pathlib import Path
from typing import List


class GeodexSheet:
    """Represents a single geodex sheet with its properties and coordinates."""
    
    def __init__(self, sheetdict: dict):
        properties = sheetdict.get("properties", {})
        self.record = properties.get("RECORD")
        self.location = properties.get("LOCATION")
        self.date = properties.get("DATE")
        self.y1 = round(properties["Y1"], 6) if properties.get("Y1") is not None else None
        self.y2 = round(properties["Y2"], 6) if properties.get("Y2") is not None else None
        self.x1 = round(properties["X1"], 6) if properties.get("X1") is not None else None
        self.x2 = round(properties["X2"], 6) if properties.get("X2") is not None else None

    def to_sheet(self) -> oimpy.MapSheet:
        # Check if all coordinates are valid numbers
        if None in [self.y1, self.y2, self.x1, self.x2]:
            raise ValueError(f"Invalid coordinates for record {self.record}")

        sheetdict = {
            "label": self.record,
            "title": self.location,
            "datePub": str(self.date),
            "north": self.y1,  # North
            "south": self.y2,  # South
            "west": self.x1,  # West
            "east": self.x2,  # East
        }
        return oimpy.MapSheet(sheetdict)
    
class GeodexGeoJSON:
    """This class represents a raw geodex feature class that has been exported to GeoJSON in QGIS"""

    def __init__(self, sheets: List[GeodexSheet]) -> None:
        self.features = sheets

    @classmethod
    def from_geojson_file(cls, geojson_file: Path) -> 'GeodexGeoJSON':
        geojson_file = Path(geojson_file)
        geodex_sheets = cls._parse_geojson_file(geojson_file)
        return cls(geodex_sheets)

    @staticmethod
    def _parse_geojson_file(geojson_file: Path) -> List[GeodexSheet]:
        geodex_sheets = []
        with geojson_file.open("r") as file:
            content_geojson = geojson.load(file)
            if isinstance(content_geojson, geojson.FeatureCollection):
                features = content_geojson.get("features", [])
                for feature in features:
                    try:
                        feature_geodex_sheet = GeodexSheet(feature)
                        geodex_sheets.append(feature_geodex_sheet)
                    except ValueError as e:
                        print(f"Skipping feature due to error: {e}")
        return geodex_sheets

    def to_openindexmap(self) -> 'oimpy.OpenIndexMap':
        valid_sheets = [sheet.to_sheet() for sheet in self.features if None not in [sheet.y1, sheet.y2, sheet.x1, sheet.x2]]
        oim = oimpy.OpenIndexMap(valid_sheets)
        return oim if oim.is_valid(schema_path) else None
        

if __name__ == "__main__":
    schema_path = "src/openindexmaps_py/1.0.0.schema.json"
    geodex_geojson_file = Path("QGIS/f0168.geojson")
    geodex_object = GeodexGeoJSON.from_geojson_file(geodex_geojson_file)
    print(f"validating OpenIndexMap against {schema_path}")
    oim = geodex_object.to_openindexmap()
    if not oim is None:
        print("oim is valid, writing to file...") 
        with open("QGIS/output.geojson", "w") as file:
            file.write(str(oim))
    else:
        print("Unable to create valid OpenIndexMap...")