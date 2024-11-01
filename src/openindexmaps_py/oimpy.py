from pathlib import Path
import json
import geojson
from geojson import FeatureCollection, Feature, Polygon
from geojson_rewind import rewind
import logging
from jsonschema import validate, ValidationError
import antimeridian
from shapely.geometry import shape
import yaml

import importlib.resources as pkg_resources

# Load the configuration from the YAML file
with pkg_resources.files('openindexmaps_py').joinpath('config.yml').open('r') as f:
    config = yaml.safe_load(f)

# Configure logging
logging.basicConfig(level=config["logging-level"])
logger = logging.getLogger(__name__)


class Sheet(Feature):
    """
    A class to represent a map sheet, inheriting from geojson.Feature.
    """

    def __init__(self, sheetdict: dict = None, **kwargs):
        # Extract geometry and properties for the GeoJSON Feature
        sheetdict = sheetdict if sheetdict else self.default_sheet_dict()
        geometry = Polygon(
            [
                [
                    (sheetdict.get("west", 0.0), sheetdict.get("south", 0.0)),
                    (sheetdict.get("east", 0.0), sheetdict.get("south", 0.0)),
                    (sheetdict.get("east", 0.0), sheetdict.get("north", 0.0)),
                    (sheetdict.get("west", 0.0), sheetdict.get("north", 0.0)),
                    (sheetdict.get("west", 0.0), sheetdict.get("south", 0.0)),
                ]
            ]
        )
        if config["fix-antimeridian"]:
            logging.debug(f"Fixing antimeridian for geometry:\n{geometry}")
            geometry = antimeridian.fix_geojson(geometry)

        properties = {
            k: v
            for k, v in sheetdict.items()
            if k not in ["type", "geometry", "properties"]
        }
        properties.update(kwargs)

        # Initialize the geojson.Feature
        super().__init__(geometry=geometry, properties=properties)

        # Set additional attributes directly
        self.label = properties.get("label", None)
        self.labelAlt = properties.get("labelAlt", None)
        self.labelAlt2 = properties.get("labelAlt2", None)
        self.datePub = properties.get("datePub", None)
        self.date = properties.get("date", None)
        self.west = self._round_if_float(properties.get("west", None))
        self.east = self._round_if_float(properties.get("east", None))
        self.north = self._round_if_float(properties.get("north", None))
        self.south = self._round_if_float(properties.get("south", None))
        self.location = properties.get("location", None)
        self.scale = properties.get("scale", None)
        self.color = properties.get("color", None)
        self.inst = properties.get("inst", None)
        self.sheetId = properties.get("sheetId", None)
        self.available = properties.get("available", None)
        self.physHold = properties.get("physHold", None)
        self.digHold = properties.get("digHold", None)
        self.instCallNo = properties.get("instCallNo", None)
        self.recId = properties.get("recId", None)
        self.download = properties.get("download", None)
        self.websiteUrl = properties.get("websiteUrl", None)
        self.thumbUrl = properties.get("thumbUrl", None)
        self.iiifUrl = properties.get("iiifUrl", None)
        self.fileName = properties.get("fileName", None)
        self.note = properties.get("note", None)

        # Add any additional attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

        if config["sheet-validation-warn"]:
            if not super().is_valid:
                logger.warning(
                    f"The sheet \"{self.label if self.label else 'Null'}\" is invalid according to geojson spec."
                )

    def default_sheet_dict(self) -> dict:
        """Provides a default metadata structure based on common fields."""
        return {
            "label": "",
            "title": "",
            "location": [],
            "datePub": "",
            "available": "",
            "west": 0.0,
            "east": 1.0,
            "north": 1.0,
            "south": 0.0,
        }

    @staticmethod
    def _round_if_float(value):
        return round(value, 6) if isinstance(value, float) else value

    @property
    def __geo_interface__(self):
        """
        Overriding the __geo_interface__ property to ensure "type" is "Feature".
        """
        return {
            "type": "Feature",
            "geometry": self.geometry,
            "properties": self.properties,
        }

    def __str__(self) -> str:
        return rewind(geojson.dumps(self, indent=4))


class MapSheet(Sheet):
    """
    A class to represent a map sheet with additional attributes.
    """

    def __init__(self, sheetdict: dict, **kwargs):
        super().__init__(sheetdict, **kwargs)
        self.title = sheetdict.get("title", None)
        self.titleAlt = sheetdict.get("titleAlt", None)
        self.dateSurvey = sheetdict.get("dateSurvey", None)
        self.datePhoto = sheetdict.get("datePhoto", None)
        self.dateReprnt = sheetdict.get("dateReprnt", None)
        self.overprint = sheetdict.get("overprint", None)
        self.edition = sheetdict.get("edition", None)
        self.publisher = sheetdict.get("publisher", None)
        self.overlays = sheetdict.get("overlays", None)
        self.projection = sheetdict.get("projection", None)
        self.lcCallNo = sheetdict.get("lcCallNo", None)
        self.contLines = sheetdict.get("contLines", None)
        self.contInterv = sheetdict.get("contInterv", None)
        self.bathLines = sheetdict.get("bathLines", None)
        self.bathInterv = sheetdict.get("bathInterv", None)
        self.primeMer = sheetdict.get("primeMer", None)


class PhotoFrame(Sheet):
    """
    A class to represent a photo frame sheet with additional attributes.
    """

    def __init__(self, sheetdict: dict, **kwargs):
        super().__init__(sheetdict, **kwargs)
        self.photomos = sheetdict.get("photomos", None)
        self.bands = sheetdict.get("bands", None)
        self.rectificn = sheetdict.get("rectificn", None)
        self.rollNo = sheetdict.get("rollNo", None)


class OpenIndexMap(FeatureCollection):
    """
    A class to represent an OpenIndexMap, inheriting from geojson.FeatureCollection.
    Contains multiple Sheet objects.
    """

    def __init__(self, sheets: list = None, **kwargs):
        sheets = sheets if sheets else self.default_oim()
        features = [sheet for sheet in sheets if isinstance(sheet, geojson.Feature)]
        super().__init__(features=features, **kwargs)

    def default_oim(self):
        return {"type": "FeatureCollection", "features": []}

    def add_sheet(self, sheet: geojson.Feature):
        if isinstance(sheet, geojson.Feature):
            self.features.append(sheet)
        else:
            raise ValueError("Only Feature objects can be added.")

    @property
    def __geo_interface__(self):
        """
        Overriding the __geo_interface__ property to ensure "type" is "FeatureCollection".
        """
        return {
            "type": "FeatureCollection",
            "features": [feature.__geo_interface__ for feature in self.features],
        }

    @classmethod
    def from_file(cls, file_path: str):
        """Creates an instance of an OpenIndexMap from a GeoJSON file."""
        with open(file_path, "r") as file:
            json_data = json.load(file)
            sheetlist = []
            for feature in json_data.get("features"):
                feature_sheet = Sheet(feature.get("properties"))
                sheetlist.append(feature_sheet)

            return cls(sheetlist)

    def __str__(self) -> str:
        return rewind(geojson.dumps(self))

    def is_valid(self, schema_path: str = "schemas/1.0.0.schema.json") -> bool:
        """
        Override the is_valid method to add custom validation logic.
        First, use the parent class's validation. Then, validate against a JSON Schema.
        """
        if super().is_valid:
            logger.info("The FeatureCollection is valid according to geojson.")
            try:
                # Load the schema from the given path
                with open(schema_path, "r") as schema_file:
                    schema = json.load(schema_file)

                # Validate the FeatureCollection against the schema
                validate(instance=self.__geo_interface__, schema=schema)
                logger.info(
                    "The FeatureCollection is valid according to the JSON Schema."
                )
                return True
            except ValidationError as e:
                logger.error(f"JSON Schema validation error: {e.message}")
                return False
            except DeprecationWarning as e:
                logger.error("JSON Schema Reference Error (TODO!)")
            except Exception as e:
                logger.error(f"Error reading schema file: {e}")
                return False
        else:
            logger.error("The FeatureCollection is not valid according to geojson.")
            return False

    def compute_bbox(self) -> list[float]:
        # Initialize variables to store min and max coordinates
        minx, miny, maxx, maxy = (
            float("inf"),
            float("inf"),
            float("-inf"),
            float("-inf"),
        )

        # Iterate through each feature in the GeoJSON
        for feature in self.__geo_interface__["features"]:
            geom = shape(feature["geometry"])
            bbox = geom.bounds
            minx, miny = min(minx, bbox[0]), min(miny, bbox[1])
            maxx, maxy = max(maxx, bbox[2]), max(maxy, bbox[3])

        # Return the bounding box in the format [minx, miny, maxx, maxy]
        return [float(minx), float(miny), float(maxx), float(maxy)]


if __name__ == "__main__":
    pass
