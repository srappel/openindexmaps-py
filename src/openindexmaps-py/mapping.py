import folium, webbrowser

from folium.plugins import MousePosition, MiniMap

import requests


def main(geojson_data):
    m = folium.Map(location=(22, -80), tiles="cartodb positron")

    geojson_object = folium.GeoJson(
        geojson_data,
        name="Cuba Military Map",
        zoom_on_click=True,
        style_function=lambda feature: {
            "fillColor": "green"
            if "sheet 6" in feature["properties"]["label"].lower()
            else "grey",
            "color": "black",
            "weight": 2,
        },
        highlight_function=lambda feature: {
            "fillColor": "red",
            "weight": 4,
        },
    )

    tooltip = folium.GeoJsonTooltip(
        fields=[
            "label",
            "datePub",
            "scale",
            "digHold",
            "location",
        ],
        aliases=["Sheet", "Published Date", "Scale", "Link", "Location(s)"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    ).add_to(geojson_object)

    # folium.features.GeoJsonPopup(
    #     fields=[
    #         "label",
    #         "datePub",
    #         "scale",
    #         "digHold",
    #     ],
    #     aliases=[
    #         "Sheet",
    #         "Published Date",
    #         "Scale",
    #         "Link"
    #     ],
    #     labels=True,
    #     style="background-color: yellow;"
    # ).add_to(geojson_object)

    geojson_object.add_to(m)

    folium.FitBounds(geojson_object.get_bounds()).add_to(m)

    folium.LayerControl().add_to(m)

    MousePosition().add_to(m)

    MiniMap(toggle_display=True).add_to(m)

    m.save("index.html")


if __name__ == "__main__":
    geojson_data = requests.get(
        "https://raw.githubusercontent.com/UWM-Libraries/OpenIndexMaps/main/233bA62500a.geojson"
    ).json()

    main(geojson_data)

    webbrowser.open("index.html")
