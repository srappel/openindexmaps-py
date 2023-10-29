"""
Test Features for openindexmaps-py
"""


class SimpleGeodexTestSheets:
    gdx_sheet: dict = {
        "record": "14924",
        "location": "LAKE MICHIGAN, MILWAUKEE HARBOR",
        "date": 1991,
        "y1": 43.075,  # North
        "y2": 42.975,  # South
        "x1": -87.95,  # West
        "x2": -87.85,  # East
    }

    antimeridian_sheet: dict = {
        "record": "999",
        "location": "Antimeridian Test Sheet",
        "date": 1989,
        "y1": 5.0,  # North
        "y2": -5.0,  # South
        "x1": 178,  # West
        "x2": -178,  # East
    }

    inset_map_sheet: dict = {
        "record": "998",
        "location": "Inset Map Test Sheet",
        "date": 1990,
        "y1": 43,  # North
        "y2": 42,  # South
        "x1": -88,  # West
        "x2": -87,  # East
        "inset": [
            {
                "inset_label": "North of Milwaukee",
                "y1": 44,
                "y2": 43.5,
                "x1": -88,
                "x2": -87.5,
            }
        ],
    }

    two_inset_map_sheet: dict = {
        "record": "997",
        "location": "Two Inset Map Test Sheet",
        "date": 1991,
        "y1": 43,  # North
        "y2": 42,  # South
        "x1": -88,  # West
        "x2": -87,  # East
        "inset": [
            {
                "inset_label": "North of Milwaukee",
                "y1": 44,
                "y2": 43.5,
                "x1": -88,
                "x2": -87.5,
            },
            {
                "inset_label": "South of Milwaukee",
                "y1": 41,
                "y2": 40.5,
                "x1": -88,
                "x2": -87.5,
            },
        ],
    }

    nonstandard_gdx_sheet: dict = {
        "record": "666",
        "location": "Târgoviște, Județul Dâmbovița, România",
        "date": 1476,
        "y1": 44.85,  # South, not North
        "y2": 44.95,  # North, not South
        "x1": 25.45,  # East, not West
        "x2": 25.55,  # West, not East
    }
