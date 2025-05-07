import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

# bounds format: [south, north, west, east]
country_bounding_boxes = {
    "Southeast Asia": [-11.5, 28.5, 92, 141],
    "Brunei": [4, 5.5, 114, 115.5],
    "Cambodia": [10, 14.5, 102.5, 107.5],
    "Indonesia": [-11.5, 6.5, 94, 141],
    "Laos": [14, 22.5, 100, 107.5],
    "Malaysia": [0.5, 8.5, 98.5, 119.5],
    "Myanmar": [9.5, 28.5, 92, 101],
    "Philippines": [5, 20, 116.5, 127],
    "Singapore": [1.2, 1.5, 103.6, 104.1],
    "Thailand": [5.5, 20.5, 97, 106],
    "Timor-Leste": [-9.5, -8, 124, 127.5],
    "Vietnam": [8.5, 23.5, 102, 110],
}


def get_country_bounds(country):
    if country in country_bounding_boxes:
        return country_bounding_boxes[country]

    try:
        geolocator = Nominatim(user_agent="map_viewer")
        location = geolocator.geocode(country, exactly_one=True)
        if location and location.raw.get("boundingbox"):
            return [float(coord) for coord in location.raw["boundingbox"]]
        return None
    except GeocoderTimedOut:
        return None


def create_map(latitude, longitude, country):
    try:
        # Get country bounds
        bounds = get_country_bounds(country)
        print(bounds)

        center_latitude = (bounds[0] + bounds[1]) / 2
        center_longitude = (bounds[2] + bounds[3]) / 2

        # Create a map centered at the given coordinates with zoom controls disabled
        m = folium.Map(
            width=1000,
            height=1000,
            location=[center_latitude, center_longitude],
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

        # Add custom CSS to make the map container square and hide controls
        m.get_root().html.add_child(
            folium.Element("""
            <style>
                body {
                    margin: 0;
                    padding: 0;
                }
                .leaflet-control-container {
                    display: none !important;
                }
                .leaflet-control-attribution {
                    display: none !important;
                }
            </style>
        """)
        )

        # Save the map to a temporary HTML file
        temp_html = "temp_map.html"
        m.save(temp_html)

        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument(
            "--window-size=1000,1000"
        )  # Set window size to match map size
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "--disable-infobars"
        )  # Remove the automation notification bar
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )  # Remove automation flags
        chrome_options.add_experimental_option(
            "useAutomationExtension", False
        )  # Disable automation extension

        # Initialize the Chrome driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options,
        )

        # Load the HTML file
        driver.get(f"file://{os.path.abspath(temp_html)}")

        # Wait for the map to load and zoom to be applied
        time.sleep(2)

        # Take screenshot
        output_file = f"{country.lower()}_map.png"
        driver.save_screenshot(output_file)

        # Clean up
        driver.quit()
        os.remove(temp_html)

        print(f"Map has been saved to {output_file}")

    except Exception as e:
        print(f"Error creating map: {str(e)}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python map.py <latitude> <longitude> <country>")
        print("Example: python map.py 40.7128 -74.0060 'United States'")
        sys.exit(1)

    try:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        country = sys.argv[3]

        create_map(latitude, longitude, country)

    except ValueError:
        print("Error: Latitude and longitude must be valid numbers")
        sys.exit(1)


if __name__ == "__main__":
    main()
