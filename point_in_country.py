import folium
from utils import get_country_bounds, take_map_screenshot


def point_in_country(latitude, longitude, country):
    # Get country bounds
    bounds = get_country_bounds(country)

    # Create a map centered at the given coordinates with zoom controls disabled
    m = folium.Map(
        width=1000,
        height=1000,
        location=[latitude, longitude],
        zoom_start=6,  # Start with a default zoom
        zoom_control=False,
        attribution_control=False,
        tiles="CartoDB voyager no-labels",
        zoom_snap=0.1,  # Allow zoom levels in 0.1 increments
    )

    # Fit bounds to show the country
    m.fit_bounds(
        [[bounds[0], bounds[2]], [bounds[1], bounds[3]]], padding=(50, 50)
    )

    # Draw rectangle around the bounding box
    folium.Rectangle(
        bounds=[[bounds[0], bounds[2]], [bounds[1], bounds[3]]],
        color="red",
        weight=2,
        fill=False,
        opacity=1,
    ).add_to(m)

    # Add a marker at the specified location
    folium.Marker(
        [latitude, longitude],
        popup=f"Location: {latitude}, {longitude}",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)

    take_map_screenshot(m, country)
