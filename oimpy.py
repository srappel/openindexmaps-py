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
        properties_dict = {}

        for key, val in sheetdict.items():
            if val.__class__ == float:
                val = round(val, 6)

            print(f"Setting atribute... {key}:{val} ({val.__class__})")
            self.__setattr__(key, val)

            properties_dict[key] = val

        self.properties_dict = properties_dict

    def __str__(self) -> str:
        """
        Returns geojson representation as str
        """
        return sheet.to_geojson_polygon_feature()

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
            properties=self.properties_dict,
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
    #print(f"\nto_geojson_polygon_feature() output:\n{sheet.to_geojson_polygon_feature()}\n")

    print(f"\n__geo_interface__ output:\n{sheet.__geo_interface__}\n")

    print(f"\nClass of sheet: {str(sheet.__class__)}")

    print(f"\n__str__ output:\n{str(sheet)}")

    # fmt:on
