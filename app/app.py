import streamlit as st
from streamlit_folium import folium_static
import folium
import geocoder
from shapely.geometry import Point, Polygon

from map import folium_base_map

st.set_page_config(layout="centered", initial_sidebar_state="expanded")
st.title("Geocoder comparison")
st.text("")

st.write(
    "Enter a place, street or address and see if the results of differenct geocoders give different results!"
)
st.text("")

address_input = st.text_input("Enter address and press Enter", "Pariser Platz, Berlin")
st.text("")
st.text("")


api_names = ["🔴 Arcgis", "🟡 OSM", "🟢 GeocodeFarm"]
a = geocoder.arcgis(address_input)
o = geocoder.osm(address_input)
g = geocoder.geocodefarm(address_input)
api_results = [a, o, g]


points = []
api_cols = st.beta_columns(3)
for col, name, result in zip(api_cols, api_names, api_results):
    col.markdown(f"## {name}")

    result = result.json
    if result is not None:
        col.markdown(f"**Address**: \n\n {result['address']}")
        col.markdown(f"**Longitude, Latitude**: \n\n {result['lng']}, {result['lat']}")
        col.text("")

        expander = col.beta_expander("Show full information")
        expander.json(result)

        points.append(Point(result["lat"], result["lng"]))
    else:
        col.markdown("Query not successful!")
        points.append(None)


colors = ["#ff0000", "#fffc00", "#40ff00"]
if points:
    centroid = Polygon([[p.x, p.y] for p in points if p is not None]).centroid

    m = folium_base_map(lat=centroid.x, lon=centroid.y, zoom_start=15)

    for name, point, color in zip(api_names, points, colors):
        folium.CircleMarker(
            location=(point.x, point.y),
            radius=12,
            popup=name,
            color=color,
            fill=True,
            fill_color=color,
        ).add_to(m)

st.text("")
st.text("")
st.text("")


folium_static(m)
