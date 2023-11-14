import testfeatures
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


class Sheet:
    label: str
    labelAlt: str
    labelAlt2: str
    datePub: str
    date: str
    west: float
    east: float
    north: float
    south: float
    location: list
    scale: str
    color: str

    # Institutional fields
    inst: str
    sheetId: str
    available: bool
    physHold: str
    digHold: str
    instCallNo: str
    recId: str
    download: str
    websiteUrl: str
    thumbUrl: str
    iiifUrl: str
    fileName: str
    note: str

    def __init__(self, sheetdict):
        self.label = sheetdict["label"]
        self.title = sheetdict["title"]
        self.datePub = sheetdict["datePub"]
        self.north = round(sheetdict["north"], 6)
        self.south = round(sheetdict["south"], 6)
        self.west = round(sheetdict["west"], 6)
        self.east = round(sheetdict["east"], 6)
        self.properties_dict: dict = {
            "label": self.label,
            "title": self.title,
            "datePub": self.datePub,
            "west": self.west,
            "east": self.east,
            "north": self.north,
            "south": self.south,
        }

    @property
    def __geo_interface__(self):
        return {
            "type": "feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        (self.south, self.west),
                        (self.south, self.east),
                        (self.north, self.east),
                        (self.north, self.west),
                        (self.south, self.west),
                    ]
                ],
            },
            "properties": self.properties_dict,
        }

    def to_geojson_polygon_feature(self):
        bbox = Polygon(
            [
                [
                    (self.south, self.west),
                    (self.south, self.east),
                    (self.north, self.east),
                    (self.north, self.west),
                    (self.south, self.west),
                ]
            ]
        )

        feature = Feature(
            geometry=bbox,
            properties={
                "label": self.label,
                "title": self.title,
                "datePub": self.datePub,
                "west": self.west,
                "east": self.east,
                "north": self.north,
                "south": self.south,
            },
        )

        if feature.is_valid:
            return rewind(geojson.dumps(feature))
        else:
            raise Exception("Non-valid feature")


class MapSheet(Sheet):
    title: str
    titleAlt: str
    dateSurvey: str
    datePhoto: str
    dateReprint: str
    overprint: str
    edition: str
    publisher: str
    overlays: str
    projection: str
    lcCallNo: str
    ontLines: bool
    contInterv: str
    bathLines: bool
    bathInterv: str
    primeMer: str


class PhotoFrame(Sheet):
    photomos: bool
    bands: str
    rectificn: bool
    rollNo: str


if __name__ == "__main__":
    sheet = MapSheet(testfeatures.SimpleTestMapSheets.sheet)
    # fmt:off
    print(f"\nto_geojson_polygon_feature() output:\n{sheet.to_geojson_polygon_feature()}\n")

    print(f"\n__geo_interface__ output:\n{sheet.__geo_interface__}")
    # fmt:on
