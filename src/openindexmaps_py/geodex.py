from openindexmaps_py import oimpy
from openindexmaps_py import testfeatures
import geojson
from pathlib import Path


def from_geojson_file(geojson_file: Path) -> geojson.feature.FeatureCollection:
    geojson_file = Path(geojson_file)
    with geojson_file.open("r") as file:
        content = file.read()
        return geojson.loads(content)


class GeodexSheet:
    def __init__(self, sheetdict: dict):
        properties = sheetdict.get("properties", None)
        self.record = properties.get("RECORD", None)
        self.location = properties.get("LOCATION", None)
        self.date = properties.get("DATE", None)
        self.y1 = round(properties.get("Y1", None), 6)
        self.y2 = round(properties.get("Y1", None), 6)
        self.x1 = round(properties.get("Y1", None), 6)
        self.x2 = round(properties.get("Y1", None), 6)

    def to_sheet(self) -> oimpy.MapSheet:
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
    
class GeodexGeoJSON():
    """This class represents a raw geodex feature class that has been exported to GeoJSON in QGIS"""
    def __init__(self) -> None:
        pass

    def to_openindexmap(self) -> oimpy.OpenIndexMap:
        pass

if __name__ == "__main__":
    schema_path = "src/openindexmaps-py/1.0.0.schema.json"
    geodex_geojson_file = "QGIS/f0168.geojson"
    geodex_geojson = from_geojson_file(geodex_geojson_file)
    geodex_geojson_sheet1 = geodex_geojson.features[1]
    sheet1_GeodexSheet = GeodexSheet(geodex_geojson_sheet1)
    sheet1_oimpySheet = sheet1_GeodexSheet.to_sheet()
    if sheet1_oimpySheet.is_valid:
        print(sheet1_oimpySheet)
    else:
        print("Sheet is not valid!")