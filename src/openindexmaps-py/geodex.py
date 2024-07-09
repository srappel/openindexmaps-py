import oimpy
import testfeatures
import geojson
from pathlib import Path


def from_geojson_file(geojson_file: Path) -> geojson.feature.FeatureCollection:
    with geojson_file.open("r") as file:
        content = file.read()
        return geojson.loads(content)


class GeodexSheet:
    def __init__(self, sheetdict: dict):
        self.record = sheetdict["record"]
        self.location = sheetdict["location"]
        self.date = sheetdict["date"]
        self.y1 = round(sheetdict["y1"], 6)
        self.y2 = round(sheetdict["y2"], 6)
        self.x1 = round(sheetdict["x1"], 6)
        self.x2 = round(sheetdict["x2"], 6)

    def to_sheet(self) -> oimpy.MapSheet:
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
    gdx_sheet = GeodexSheet(testfeatures.SimpleGeodexTestSheets.gdx_sheet)
    gdx_sheet_object = gdx_sheet.to_sheet()
    gdx_oim = oimpy.OpenIndexMap([gdx_sheet_object])
    print(gdx_oim)
