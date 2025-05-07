import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
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

def string_to_camel_case(string):
    return '_'.join(word.lower() for word in string.replace(' ', '_').replace('-', '_').split('_'))

def find_next_name(filename_prefix):
    index = 1
    while os.path.exists(f"maps/{filename_prefix}_{index}.png"):
        index += 1
    return f"{filename_prefix}_{index}"

def take_map_screenshot(m, filename_prefix):
    try:
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

        if not os.path.exists("maps"):
            os.makedirs("maps")

        print(string_to_camel_case(filename_prefix))
        filename = find_next_name(string_to_camel_case(filename_prefix))

        # Take screenshot
        output_file = f"maps/{filename}.png"
        driver.save_screenshot(output_file)

        # Clean up
        driver.quit()
        os.remove(temp_html)

        print(f"Map has been saved to {output_file}")

    except Exception as e:
        print(f"Error creating map: {str(e)}")