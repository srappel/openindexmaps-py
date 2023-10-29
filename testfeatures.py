"""
Test Features for openindexmaps-py
"""


class SimpleGeodexTestSheets:
    gdx_sheet: dict = {
        "record": "14924",
        "location": "LAKE MICHIGAN, MILWAUKEE HARBOR",
        "date": 1991,
        "y1": 43.075,
        "y2": 42.975,
        "x1": -87.95,
        "x2": -87.85,
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
