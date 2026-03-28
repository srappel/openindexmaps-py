from copy import deepcopy
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
from openindexmaps_py.resources import resolve_schema_resource

DEFAULT_SCHEMA_NAME = "1.0.0.schema.json"

# Load the configuration from the YAML file
with pkg_resources.files("openindexmaps_py").joinpath("config.yml").open("r") as f:
    config = yaml.safe_load(f)

logger = logging.getLogger(__name__)


class Sheet(Feature):
    """
    A class to represent a map sheet, inheriting from geojson.Feature.
    """

    def __init__(
        self, sheetdict: dict = None, collection_crs: dict | None = None, **kwargs
    ):
        feature = sheetdict if self._looks_like_feature(sheetdict) else None
        sheetdict = sheetdict if sheetdict else self.default_sheet_dict()
        spatially_geographic, spatial_reason = self._is_spatially_geographic(
            feature if feature is not None else sheetdict,
            collection_crs=collection_crs,
        )
        geometry = (
            self._normalize_feature_geometry(
                feature.get("geometry"),
                spatially_geographic=spatially_geographic,
                spatial_reason=spatial_reason,
                feature_label=self._feature_label(feature),
            )
            if feature is not None
            else self._geometry_from_bbox(sheetdict)
        )

        properties = (
            dict(feature.get("properties", {}))
            if feature is not None
            else {
                k: v
                for k, v in sheetdict.items()
                if k not in ["type", "geometry", "properties"]
            }
        )
        properties.update(kwargs)

        # Initialize the geojson.Feature
        super().__init__(geometry=geometry, properties=properties)
        self.collection_crs = collection_crs
        self.spatially_geographic = spatially_geographic
        self.spatial_reason = spatial_reason

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

    @classmethod
    def from_feature(cls, feature: dict, collection_crs: dict | None = None, **kwargs):
        return cls(feature, collection_crs=collection_crs, **kwargs)

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

    @staticmethod
    def _feature_label(feature: dict | None) -> str:
        if not isinstance(feature, dict):
            return "Unknown"
        properties = feature.get("properties", {})
        if isinstance(properties, dict):
            return str(
                properties.get("label") or properties.get("sheetId") or "Unknown"
            )
        return "Unknown"

    @staticmethod
    def _looks_like_feature(sheetdict: dict | None) -> bool:
        return isinstance(sheetdict, dict) and (
            "geometry" in sheetdict or "properties" in sheetdict
        )

    @staticmethod
    def _geometry_from_bbox(sheetdict: dict) -> dict:
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
        return geometry

    @staticmethod
    def _crs_name(crs: dict | None) -> str | None:
        if not isinstance(crs, dict):
            return None
        properties = crs.get("properties", {})
        if isinstance(properties, dict):
            name = properties.get("name")
            if isinstance(name, str):
                return name
        return None

    @classmethod
    def _is_wgs84_crs(cls, crs: dict | None) -> bool:
        crs_name = cls._crs_name(crs)
        if crs_name is None:
            return False

        normalized_name = crs_name.upper()
        return any(
            token in normalized_name
            for token in ("EPSG:4326", "CRS84", "WGS84", "WGS 84")
        )

    @classmethod
    def _iter_positions(cls, coordinates):
        if not isinstance(coordinates, list):
            return
        if coordinates and all(
            isinstance(value, (int, float)) for value in coordinates[:2]
        ):
            yield coordinates
            return
        for item in coordinates:
            yield from cls._iter_positions(item)

    @classmethod
    def _geometry_looks_geographic(cls, geometry: dict | None) -> bool:
        if not isinstance(geometry, dict):
            return False
        coordinates = geometry.get("coordinates")
        if coordinates is None:
            return False

        found_position = False
        for position in cls._iter_positions(coordinates):
            found_position = True
            lon, lat = position[:2]
            if not (-180 <= lon <= 180 and -90 <= lat <= 90):
                return False
        return found_position

    @classmethod
    def _is_spatially_geographic(
        cls, sheetdict: dict, collection_crs: dict | None = None
    ) -> tuple[bool, str]:
        crs = sheetdict.get("crs") if isinstance(sheetdict, dict) else None
        crs = crs if crs is not None else collection_crs

        if crs is not None:
            if cls._is_wgs84_crs(crs):
                return True, "WGS84-like CRS"
            return False, f"non-geographic CRS declared: {cls._crs_name(crs) or crs}"

        geometry = sheetdict.get("geometry") if isinstance(sheetdict, dict) else None
        if geometry is None:
            return True, "bbox-generated geometry"

        if cls._geometry_looks_geographic(geometry):
            return True, "coordinate ranges look geographic"

        return False, "coordinate ranges are outside lon/lat bounds"

    @staticmethod
    def _normalize_feature_geometry(
        geometry: dict | None,
        *,
        spatially_geographic: bool,
        spatial_reason: str,
        feature_label: str = "Unknown",
    ) -> dict | None:
        if geometry is None:
            return None

        geometry = deepcopy(geometry)
        geometry_type = geometry.get("type")

        if not spatially_geographic:
            logger.warning(
                'Skipping geographic normalization for sheet "%s": %s',
                feature_label,
                spatial_reason,
            )
            return geometry

        if config["fix-antimeridian"] and geometry_type in {"Polygon", "MultiPolygon"}:
            logger.warning(
                'Applying antimeridian normalization to sheet "%s" (%s)',
                feature_label,
                geometry_type,
            )
            logging.debug(f"Fixing antimeridian for geometry:\n{geometry}")
            geometry = antimeridian.fix_geojson(geometry)

        return geometry

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

    def __init__(self, sheets: list = None, crs: dict | None = None, **kwargs):
        sheets = sheets if sheets else self.default_oim()
        features = [sheet for sheet in sheets if isinstance(sheet, geojson.Feature)]
        super().__init__(features=features, **kwargs)
        self.crs = crs

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
            if json_data.get("crs") is not None:
                crs_name = Sheet._crs_name(json_data.get("crs")) or str(
                    json_data.get("crs")
                )
                logger.warning("Loaded GeoJSON with declared CRS: %s", crs_name)
            sheetlist = []
            for feature in json_data.get("features"):
                feature_sheet = Sheet.from_feature(
                    feature, collection_crs=json_data.get("crs")
                )
                sheetlist.append(feature_sheet)

            return cls(sheetlist, crs=json_data.get("crs"))

    def __str__(self) -> str:
        return rewind(geojson.dumps(self))

    def is_valid(self, schema_path: str | None = None) -> bool:
        """
        Override the is_valid method to add custom validation logic.
        First, use the parent class's validation. Then, validate against a JSON Schema.
        """
        if super().is_valid:
            logger.info("The FeatureCollection is valid according to geojson.")
            try:
                schema_resource = resolve_schema_resource(
                    schema_path, DEFAULT_SCHEMA_NAME
                )

                # Load the schema from the given path
                with schema_resource.open("r", encoding="utf-8") as schema_file:
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
        for feature in self.features:
            if isinstance(feature, Sheet) and not feature.spatially_geographic:
                logger.warning(
                    'Refusing geographic bbox computation for sheet "%s": %s',
                    feature.label if feature.label else "Unknown",
                    feature.spatial_reason,
                )
                raise ValueError(
                    f"Cannot compute a geographic bbox for non-geographic geometry: {feature.spatial_reason}"
                )

            feature_geo_interface = (
                feature.__geo_interface__
                if hasattr(feature, "__geo_interface__")
                else feature
            )

            if not isinstance(feature, Sheet):
                spatially_geographic, spatial_reason = Sheet._is_spatially_geographic(
                    feature_geo_interface,
                    collection_crs=self.crs,
                )
                if not spatially_geographic:
                    logger.warning(
                        "Refusing geographic bbox computation for feature without Sheet wrapper: %s",
                        spatial_reason,
                    )
                    raise ValueError(
                        f"Cannot compute a geographic bbox for non-geographic geometry: {spatial_reason}"
                    )

            geom = shape(feature_geo_interface["geometry"])
            bbox = geom.bounds
            minx, miny = min(minx, bbox[0]), min(miny, bbox[1])
            maxx, maxy = max(maxx, bbox[2]), max(maxy, bbox[3])

        # Return the bounding box in the format [minx, miny, maxx, maxy]
        return [float(minx), float(miny), float(maxx), float(maxy)]
