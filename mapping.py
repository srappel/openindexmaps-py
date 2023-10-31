import folium
import requests

m = folium.Map(location=(22, -80), tiles="cartodb positron", zoom_start=7)

geojson_data = requests.get(
    "https://raw.githubusercontent.com/UWM-Libraries/OpenIndexMaps/main/233bA62500a.geojson"
).json()

fgj = folium.GeoJson(
    geojson_data,
    name="Cuba Military Map",
)

fgj.add_child(folium.Popup("test"))

folium.features.GeoJsonPopup(
    fields=[
        "label",
        "datePub",
        "scale",
        "digHold",
    ],
    labels=True,
).add_to(fgj)

print()

fgj.add_to(m)

folium.LayerControl().add_to(m)

m.save("index.html")
