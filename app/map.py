import folium
from folium.plugins import Draw


def folium_base_map(
    lat: float = 52.49190032214706,
    lon: float = 13.39117252959244,
    zoom_start: int = 5,
    width_percent: str = "95%",
    layer_control=False,
) -> folium.Map:
    """Provides a folium map with basic features."""
    mapfigure = folium.Figure(width=width_percent)
    m = folium.Map(location=[lat, lon], zoom_start=zoom_start, crs="EPSG3857").add_to(
        mapfigure
    )

    folium.TileLayer(
        tiles="OpenStreetMap", attr="OpenStreetMap", name="Satellite - ESRI"
    ).add_to(m)

    formatter = "function(num) {return L.Util.formatNum(num, 4) + ' ';};"
    folium.plugins.MousePosition(
        position="bottomright",
        separator=" | ",
        empty_string="NaN",
        lng_first=True,
        num_digits=20,
        prefix="lon/lat:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)

    folium.plugins.MiniMap(
        tile_layer="OpenStreetMap", position="bottomright", zoom_level_offset=-6
    ).add_to(m)
    folium.plugins.Fullscreen().add_to(m)

    if layer_control:
        folium.LayerControl(position="bottomleft", collapsed=False, zindex=100).add_to(
            m
        )
        # If adding additional layers outside of the folium base map function, don't
        # use this one here. Causes an empty map.
    return m
