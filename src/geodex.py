import oimpy
import testfeatures
import geojson
from pathlib import Path

def from_GeoJSON(geojson_file) -> geojson.feature.FeatureCollection:
        file_data = open(geojson_file, "r")
        content = file_data.read()
        featurecollection = geojson.loads(content)
        return featurecollection

class GeodexSheet:
    record: str
    location: str
    date: int  # 4 digit year only
    y1: float  # North
    y2: float  # South
    x1: float  # West
    x2: float  # East

    def __init__(self, sheetdict):
        self.record = sheetdict["record"]
        self.location = sheetdict["location"]
        self.date = sheetdict["date"]
        self.y1 = round(sheetdict["y1"], 6)
        self.y2 = round(sheetdict["y2"], 6)
        self.x1 = round(sheetdict["x1"], 6)
        self.x2 = round(sheetdict["x2"], 6)

    def to_Sheet(self) -> oimpy.MapSheet:
        sheetdict = {
            "label": self.record,
            "title": self.location,
            "datePub": self.date,
            "north": self.y1,  # North
            "south": self.y2,  # South
            "west": self.x1,  # West
            "east": self.x2,  # East
        }
        return oimpy.MapSheet(sheetdict)


if __name__ == "__main__":
    # fmt:off
    gdxsheet = GeodexSheet(testfeatures.SimpleGeodexTestSheets.gdx_sheet)

    # print(f"Class of gdxsheet is {gdxsheet.__class__}")

    # print(f"\nto_geojson_polygon_feature() output:\n{gdxsheet.to_Sheet().to_geojson_polygon_feature()}\n")

    # print(f"\n__geo_interface__ output:\n{gdxsheet.to_Sheet().__geo_interface__}\n")

    gdx_geojson = from_GeoJSON(Path('C:/Users/srappel/Documents/GitHub/openindexmaps-py/MillionthMap.geojson'))
    print(gdx_geojson)
