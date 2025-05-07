# Map Viewer

A Python tool that displays interactive maps with markers at specified coordinates.

## Setup

This project uses `uv` as the package manager. To get started:

1. Install `uv` if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
uv pip install -e .
```

## Usage

Run the script with latitude, longitude, and country name:
```bash
python map.py 40.7128 -74.0060 "United States"
```

This will create an HTML file (e.g., `united_states_map.html`) that you can open in your web browser.

## Example Coordinates

- New York City: 40.7128, -74.0060
- London: 51.5074, -0.1278
- Tokyo: 35.6762, 139.6503 