from pathlib import Path
import geojson
from geojson import Feature, Polygon
from geojson_rewind import rewind
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Sheet:
    """
    A class to represent a sheet in an OpenIndexMap.
    """
    def __init__(self, sheetdict: dict, **kwargs):
        # Common attributes
        self.label = sheetdict.get('label', None)
        self.labelAlt = sheetdict.get('labelAlt', None)
        self.labelAlt2 = sheetdict.get('labelAlt2', None)
        self.datePub = sheetdict.get('datePub', None)
        self.date = sheetdict.get('date', None)
        self.west = self._round_if_float(sheetdict.get('west', None))
        self.east = self._round_if_float(sheetdict.get('east', None))
        self.north = self._round_if_float(sheetdict.get('north', None))
        self.south = self._round_if_float(sheetdict.get('south', None))
        self.location = sheetdict.get('location', None)
        self.scale = sheetdict.get('scale', None)
        self.color = sheetdict.get('color', None)
        self.inst = sheetdict.get('inst', None)
        self.sheetId = sheetdict.get('sheetId', None)
        self.available = sheetdict.get('available', None)
        self.physHold = sheetdict.get('physHold', None)
        self.digHold = sheetdict.get('digHold', None)
        self.instCallNo = sheetdict.get('instCallNo', None)
        self.recId = sheetdict.get('recId', None)
        self.download = sheetdict.get('download', None)
        self.websiteUrl = sheetdict.get('websiteUrl', None)
        self.thumbUrl = sheetdict.get('thumbUrl', None)
        self.iiifUrl = sheetdict.get('iiifUrl', None)
        self.fileName = sheetdict.get('fileName', None)
        self.note = sheetdict.get('note', None)

        # Add any additional attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def _round_if_float(value):
        return round(value, 6) if isinstance(value, float) else value

    def __str__(self) -> str:
        """
        Returns geojson representation as str.
        """
        return self.to_geojson_polygon_feature()

    def to_geojson_polygon_feature(self) -> str:
        """
        Converts sheet information to a GeoJSON polygon feature.
        """
        bbox = Polygon(
            [[
                (self.west, self.south),
                (self.east, self.south),
                (self.east, self.north),
                (self.west, self.north),
                (self.west, self.south),
            ]]
        )
        feature = Feature(
            geometry=bbox,
            properties=self.__dict__,
        )

        if feature.is_valid:
            return rewind(geojson.dumps(feature))
        else:
            raise ValueError("Non-valid feature")


class MapSheet(Sheet):
    """
    A class to represent a map sheet with map-specific attributes.
    """
    def __init__(self, sheetdict: dict, **kwargs):
        super().__init__(sheetdict, **kwargs)
        self.title = sheetdict.get('title', None)
        self.titleAlt = sheetdict.get('titleAlt', None)
        self.dateSurvey = sheetdict.get('dateSurvey', None)
        self.datePhoto = sheetdict.get('datePhoto', None)
        self.dateReprnt = sheetdict.get('dateReprnt', None)
        self.overprint = sheetdict.get('overprint', None)
        self.edition = sheetdict.get('edition', None)
        self.publisher = sheetdict.get('publisher', None)
        self.overlays = sheetdict.get('overlays', None)
        self.projection = sheetdict.get('projection', None)
        self.lcCallNo = sheetdict.get('lcCallNo', None)
        self.contLines = sheetdict.get('contLines', None)
        self.contInterv = sheetdict.get('contInterv', None)
        self.bathLines = sheetdict.get('bathLines', None)
        self.bathInterv = sheetdict.get('bathInterv', None)
        self.primeMer = sheetdict.get('primeMer', None)


class PhotoFrame(Sheet):
    """
    A class to represent a photo frame sheet with air photo-specific attributes.
    """
    def __init__(self, sheetdict: dict, **kwargs):
        super().__init__(sheetdict, **kwargs)
        self.photomos = sheetdict.get('photomos', None)
        self.bands = sheetdict.get('bands', None)
        self.rectificn = sheetdict.get('rectificn', None)
        self.rollNo = sheetdict.get('rollNo', None)


if __name__ == "__main__":
    import testfeatures
    sheet = MapSheet(testfeatures.SimpleTestMapSheets.sheet)

    logger.info(f"\n__str__ output:\n{str(sheet)}\n")
    logger.info(sheet.__dict__)