import geojson
from geojson import Feature, Polygon


class Sheet:
    record: str
    location: str
    date: int  # 4 digit year only
    x1: float  # West
    x2: float  # East
    y1: float  # North
    y2: float  # South

    def __init__(self, gdxdict):
        self.record = gdxdict["record"]
        self.location = gdxdict["location"]
        self.date = gdxdict["date"]
        self.x1 = round(gdxdict["x1"], 6)
        self.x2 = round(gdxdict["x2"], 6)
        self.y1 = round(gdxdict["y1"], 6)
        self.y2 = round(gdxdict["y2"], 6)

    def toGeoJSON(self):
        bbox = Polygon(
            [
                [
                    (self.x1, self.y1),  # NW
                    (self.x1, self.y2),  # SW
                    (self.x2, self.y2),  # SE
                    (self.x2, self.y1),  # NE
                    (self.x1, self.y1),  # NW
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

        dump = geojson.dumps(feature)

        return dump


if __name__ == "__main__":
    gdxsheet = {
        "record": "14924",
        "location": "LAKE MICHIGAN, MILWAUKEE HARBOR",
        "date": 1991,
        "x1": -87.95,
        "x2": -87.85,
        "y1": 43.075,
        "y2": 42.975,
    }

    simplegeodexsheet = Sheet(gdxsheet)
    gdxJSON = simplegeodexsheet.toGeoJSON()
    print(gdxJSON)
