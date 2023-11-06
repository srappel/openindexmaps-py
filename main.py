import testfeatures
from testfeatures import SimpleGeodexTestSheets as gdx
from pathlib import Path

import geojson
from geojson import Feature, Polygon, MultiPolygon
from geojson_rewind import rewind


class MapSet:
    filename: Path
    title: str
    bbox: Polygon
    maxdate: int
    mindate: int


class Sheet():
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

    @property
    def __geo_interface__(self):
        return {
            "type": "feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                (self.x1, self.y2),  # SW
                (self.x2, self.y2),  # SE
                (self.x2, self.y1),  # NE
                (self.x1, self.y1),  # NW
                (self.x1, self.y2),  # SW
            ]],
            },
            "properties": {
                "label": self.record,
                "title": self.location,
                "datepub": self.date,
                "west": self.x1,
                "east": self.x2,
                "north": self.y1,
                "south": self.y2,
            }
        }

    

    def to_geojson_polygon_feature(self):
        bbox = Polygon(
            [
                [
                    (self.x1, self.y2),  # SW
                    (self.x2, self.y2),  # SE
                    (self.x2, self.y1),  # NE
                    (self.x1, self.y1),  # NW
                    (self.x1, self.y2),  # SW
                ]
            ]
        )

        feature = Feature(
            geometry=bbox,
            properties={
                "label": self.record,
                "title": self.location,
                "datepub": self.date,
                "west": self.x1,
                "east": self.x2,
                "north": self.y1,
                "south": self.y2,
            },
        )

        if feature.is_valid:
            return rewind(geojson.dumps(feature))
        else:
            raise Exception("Non-valid feature")

    


class MapSheet(Sheet):
    title: str


class PhotoFrame(Sheet):
    photomos: bool
    bands: str
    rectificn: bool
    rollNo: str


if __name__ == "__main__":
    sheet = Sheet(gdx.antimeridian_sheet)

    print(sheet.__geo_interface__)

