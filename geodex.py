import oimpy

from oimpy import Sheet


class GeodexSheet(Sheet):
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


class GeodexConversion:
    def gdx_to_oim(sheetdict) -> dict:
        gdx_sheetdict = sheetdict

        oim_sheetdict = []
        oim_sheetdict.record = sheetdict["record"]
        oim_sheetdict.location = sheetdict["location"]
        oim_sheetdict.date = sheetdict["date"]
        oim_sheetdict.y1 = round(sheetdict["y1"], 6)
        oim_sheetdict.y2 = round(sheetdict["y2"], 6)
        oim_sheetdict.x1 = round(sheetdict["x1"], 6)
        oim_sheetdict.x2 = round(sheetdict["x2"], 6)

    def oim_to_gdx(sheetdict) -> dict:
        print("Convert a gdx class dict to a oim class dict.")
