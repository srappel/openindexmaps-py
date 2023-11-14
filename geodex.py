import oimpy
import testfeatures


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

    print(f"Class of gdxsheet is {gdxsheet.__class__}")

    print(f"\nto_geojson_polygon_feature() output:\n{gdxsheet.to_Sheet().to_geojson_polygon_feature()}\n")

    print(f"\n__geo_interface__ output:\n{gdxsheet.to_Sheet().__geo_interface__}\n")

    print("Great Success!")
