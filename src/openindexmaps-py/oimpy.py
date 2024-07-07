import geojson
from geojson import FeatureCollection, Feature, Polygon
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Sheet(Feature):
    """
    A class to represent a map sheet, inheriting from geojson.Feature.
    """
    def __init__(self, sheetdict: dict, **kwargs):
        geometry = Polygon(
            [[
                (sheetdict.get('west', 0.0), sheetdict.get('south', 0.0)),
                (sheetdict.get('east', 0.0), sheetdict.get('south', 0.0)),
                (sheetdict.get('east', 0.0), sheetdict.get('north', 0.0)),
                (sheetdict.get('west', 0.0), sheetdict.get('north', 0.0)),
                (sheetdict.get('west', 0.0), sheetdict.get('south', 0.0)),
            ]]
        )
        properties = {k: v for k, v in sheetdict.items() if k not in ['type', 'geometry', 'properties']}
        properties.update(kwargs)

        # Initialize the geojson.Feature
        super().__init__(geometry=geometry, properties=properties)

        # Set additional attributes directly
        for key, value in properties.items():
            setattr(self, key, value)

    @staticmethod
    def _round_if_float(value):
        return round(value, 6) if isinstance(value, float) else value

    def __str__(self) -> str:
        return geojson.dumps(self)


class MapSheet(Sheet):
    """
    A class to represent a map sheet with additional attributes.
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
    A class to represent a photo frame sheet with additional attributes.
    """
    def __init__(self, sheetdict: dict, **kwargs):
        super().__init__(sheetdict, **kwargs)
        self.photomos = sheetdict.get('photomos', None)
        self.bands = sheetdict.get('bands', None)
        self.rectificn = sheetdict.get('rectificn', None)
        self.rollNo = sheetdict.get('rollNo', None)


class OpenIndexMap(FeatureCollection):
    """
    A class to represent an OpenIndexMap, inheriting from geojson.FeatureCollection.
    Contains multiple Sheet objects.
    """
    def __init__(self, sheets: list, **kwargs):
        features = [sheet for sheet in sheets if isinstance(sheet, Sheet)]
        super().__init__(features=features, **kwargs)

    def add_sheet(self, sheet: Sheet):
        if isinstance(sheet, Sheet):
            self.features.append(sheet)
        else:
            raise ValueError("Only Sheet objects can be added.")

    def __str__(self) -> str:
        return geojson.dumps(self)


if __name__ == "__main__":
    import testfeatures
    sheet = MapSheet(testfeatures.SimpleTestMapSheets.sheet)
    open_index_map = OpenIndexMap(sheets=[sheet])

    logger.info(f"\nOpenIndexMap:\n{str(open_index_map)}\n")
    logger.info(open_index_map.__dict__)