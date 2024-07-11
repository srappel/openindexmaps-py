from openindexmaps_py import oimpy
import geojson
from pathlib import Path
from typing import List

class GeodexDictionary:
    """A class for looking up various geodex attributes."""
    
    def __init__(self):
        self.lookup_dict = {
            "map_type": {
                30: "Administrative map",
                1: "Aerial photograph",
                6: "Aeronautical chart",
                7: "Bathymetric map",
                21: "Coal map",
                0: "Not assigned",
                5: "Geologic map",
                4: "Hydrogeologic map",
                11: "Land use map",
                12: "Nautical chart",
                13: "Orthophoto map",
                14: "Planimetric map",
                998: "Printed map - 2 color",
                997: "Printed map - colored",
                996: "Printed map - monochrome",
                995: "Projection not indicated",
                15: "Reference map",
                16: "Road map",
                22: "Satellite image map",
                24: "Shaded relief map",
                18: "Topo map (contours)",
                23: "Topo map (form lines)",
                19: "Topo map (hachures)",
                25: "Topo map (irr interval)",
                20: "Topo map (layer tints)"
            },
            "production": {
                38: "Blue line print",
                39: "Blueprint",
                37: "Negative microform",
                35: "Negative photocopy",
                34: "Positive photocopy",
                31: "Printed map - colored",
                33: "Printed map - monochrome",
                32: "Printed map - 2 color"
            },
            "projection": {
                0: "Not assigned",
                163: "Azimuthal equidistant",
                185: "Bonne",
                199: "Cassini",
                182: "Conic equidistant",
                183: "Conic",
                171: "Cylindrical",
                180: "Gauss-Krüger",
                999: "Gauss-Krüger",
                164: "Gnomonic",
                186: "Lambert conformal conic",
                175: "Mercator",
                176: "Miller",
                998: "Munich PM",
                187: "Polyconic",
                198: "Polyhedric",
                161: "Not indicated",
                178: "Sinusoidal",
                168: "Stereographic",
                179: "Transverse Mercator"
            },
            "prime_meridian": {
                0: "Not assigned",
                157: "Athens PM",
                999: "Cordoba PM",
                148: "Copenhagen PM",
                135: "Ferro PM",
                131: "Greenwich PM",
                132: "Madrid PM",
                146: "Munich PM",
                142: "Paris PM",
                138: "Quito PM",
                147: "Rome PM"
            },
            "iso_type": {
                1: "Isobars Feet",
                2: "Isobars Fathoms",
                3: "Isobars Meters",
                4: "Contours Feet",
                5: "Contours Meters",
                6: "Multiple Isobar Types",
                7: "No Isobar Indicated"
            },
            "year_type": { 
                97: "Approximate Date", # datePub
                98: "Publication Date", # datePub
                99: "Compilation Date", # datePub
                100: "Base Map Date", # date
                102: "Field Checked", # dateSurvey
                103: "Image Year", # datePhoto
                104: "Photography to", # datePhoto
                105: "Photo Inspected", # datePhoto
                106: "Image Date", # datePhoto
                108: "Preliminary Edition", # date
                109: "Compiled From Map Dated", # datePSurvey
                110: "Interim Edition", # date
                112: "Printed", # datePub
                113: "Printed Circa", # datePub
                114: "Revised", # date
                115: "Situation/Survey", # dateSurvey
                116: "Transportation Network", # date
                118: "Provisional Edition", # date
                120: "Photo Revised", # datePhoto
                121: "Edition of", # datePub
                119: "Magnetic Declination Year" # date
            }
        }

    def lookup(self, category: str, key: int) -> str:
        """Lookup a value based on category and key.
        
        Args:
            category (str): The category to lookup (e.g., 'map_type', 'production', 'projection', 'prime_meridian', 'iso_type', 'year_type').
            key (int): The key to lookup within the category.
            
        Returns:
            str: The corresponding value if found, else 'Unknown key'.
        """
        return self.lookup_dict.get(category, {}).get(key, "Unknown key")


class GeodexSheet:
    """Represents a single geodex sheet with its properties and coordinates."""
    
    def __init__(self, sheetdict: dict):
        geodex_dict = GeodexDictionary()
        properties = sheetdict.get("properties", {})

        self.record = properties.get("RECORD")
        self.location = properties.get("LOCATION")
        self.date = properties.get("DATE")
        self.y1 = round(properties["Y1"], 6) if properties.get("Y1") is not None else None
        self.y2 = round(properties["Y2"], 6) if properties.get("Y2") is not None else None
        self.x1 = round(properties["X1"], 6) if properties.get("X1") is not None else None
        self.x2 = round(properties["X2"], 6) if properties.get("X2") is not None else None
        self.scale = properties.get("SCALE", None)
        self.production = geodex_dict.lookup("production", properties.get("PRODUCTION"))
        self.holding = "true" if properties.get("HOLD") == 1 else "false"
        self.catloc = properties.get("CATLOC", None)
        self.series_tit = properties.get("SERIES_TIT", None)
        self.publisher = properties.get("PUBLISHER", None)
        self.map_type = properties.get("MAP_TYPE", None)
        self.map_for = properties.get("MAP_FOR", None)
        self.project = properties.get("PROJECT", None)
        self.prime_mer = properties.get("PRIME_MER", None)
        self.year1 = properties.get("YEAR1", None)
        self.year1_type = properties.get("YEAR1_TYPE", None)
        self.year2 = properties.get("YEAR2", None)
        self.year2_type = properties.get("YEAR2_TYPE", None)
        self.year3 = properties.get("YEAR3", None)
        self.year3_type = properties.get("YEAR3_TYPE", None)
        self.year4 = properties.get("YEAR4", None)
        self.year4_type = properties.get("YEAR4_TYPE", None)
        self.edition_no = properties.get("EDITION_NO", None)
        self.iso_type = properties.get("ISO_TYPE", None)
        self.iso_val = properties.get("ISO_VAL", 0)

    def get_dates(self) -> dict:
        oim_date_dict = {
            "datePub": [97, 98, 99, 113, 121],
            "date": [100, 110, 114, 116, 118, 119],
            "dateSurvey": [102, 109, 115],
            "datePhoto": [103, 104, 105, 106, 120],
        }

        years = [
            {"year1": (self.year1, self.year1_type)},
            {"year2": (self.year2, self.year2_type)},
            {"year3": (self.year3, self.year3_type)},
            {"year4": (self.year4, self.year4_type)},
        ]

        dates = {
            "datePub": None,
            "date": None,
            "dateSurvey": None,
            "datePhoto": None,
        }

        for year in years:
            for year_key, (year_val, year_type) in year.items():
                if year_val is None or year_type is None:
                    continue
                for date_key, type_list in oim_date_dict.items():
                    if year_type in type_list:
                        dates[date_key] = year_val

        if dates["datePub"] is None:
            dates.pop("datePub")

        # Remove keys with None values
        return {k: v for k, v in dates.items() if v is not None}
    
    def get_iso(self) -> dict:
        # "iso_type": {
        #         1: "Isobars Feet",
        #         2: "Isobars Fathoms",
        #         3: "Isobars Meters",
        #         4: "Contours Feet",
        #         5: "Contours Meters",
        #         6: "Multiple Isobar Types",
        #         7: "No Isobar Indicated"
        iso = {
            "contLines": None,
            "contInterv": None,
            "bathLines": None,
            "bathInterv": None,
        }
        geodex_dict = GeodexDictionary()
        if self.iso_type == 4:
            iso["contLines"] = "true"
            if self.iso_val != 0:
                iso["contInterv"] = f"{str(self.iso_val)} feet"
        elif self.iso_type == 5:
            iso["contLines"] = "true"
            if self.iso_val != 0:
                iso["contInterv"] = f"{str(self.iso_val)} meters"
        elif self.iso_type == 1:
            iso["bathLines"] = "true"
            if self.iso_val != 0:
                iso["bathInterv"] = f"{str(self.iso_val)} feet"
        elif self.iso_type == 2:
            iso["bathLines"] = "true"
            if self.iso_val != 0:
                iso["bathInterv"] = f"{str(self.iso_val)} fathoms"
        elif self.iso_type == 3:
            iso["bathLines"] = "true"
            if self.iso_val != 0:
                iso["bathInterv"] = f"{str(self.iso_val)} meters"
        
        # Remove keys with None values
        return {k: v for k, v in iso.items() if v is not None}
        
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
            "scale": self.scale,
            "color": self.production,
            "inst": "AGSL",
            "available": self.holding,
            "instCallNo": self.catloc,
            "edition": self.edition_no,
            "publisher": self.publisher,
            "projection": self.project,
            "primeMer": self.prime_mer,
        }
        dates = self.get_dates()
        sheetdict.update(dates)
        iso = self.get_iso()
        sheetdict.update(iso)

        sheetdict = {k: v for k, v in sheetdict.items() if v is not None}
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
