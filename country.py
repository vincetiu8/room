import folium
from utils import get_country_bounds, get_country_center, get_country_geojson, take_map_screenshot


def highlight_country(country: str):
    # Get Southeast Asia bounds
    sea_bounds = get_country_bounds("southeast asia")

    # Calculate center of Southeast Asia
    center_lat = (sea_bounds[0] + sea_bounds[1]) / 2
    center_lon = (sea_bounds[2] + sea_bounds[3]) / 2

    # Create a map centered on Southeast Asia
    m = folium.Map(
        width=1000,
        height=1000,
        location=[center_lat, center_lon],
        zoom_start=5,  # Start with a default zoom
        zoom_control=False,
        attribution_control=False,
        tiles="CartoDB voyager no-labels",
        zoom_snap=0.1,  # Allow zoom levels in 0.1 increments
    )

    # Fit bounds to show Southeast Asia
    m.fit_bounds(
        [[sea_bounds[0], sea_bounds[2]], [sea_bounds[1], sea_bounds[3]]],
        padding=(50, 50),
    )

    country_geojson = get_country_geojson(country)

    if country_geojson is None:
        print(f"Country {country} not found")
        return

    folium.GeoJson(
        country_geojson,
        style_function=lambda x: {
            "fillColor": "red",
            "color": "red",
            "weight": 2,
            "fillOpacity": 0.2,
        },
    ).add_to(m)

    # Add country name label at the center of the country
    center = get_country_center(country)

    folium.Marker(
        [center[1], center[0]],  # GeoJSON uses [lon, lat] order
        popup=country,
        icon=folium.DivIcon(
            html=f'<div style="font-size: 16pt; color: red; font-weight: bold;">{country}</div>'
        ),
    ).add_to(m)

    take_map_screenshot(m, f"{country.lower()}_highlighted")
