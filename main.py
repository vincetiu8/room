from typing import Optional

import typer

from country import highlight_country
from point_in_country import point_in_country

app = typer.Typer()


@app.command(name="point")
def point(
    latitude: float,
    longitude: float,
    country: Optional[str] = "Southeast Asia",
):
    country = country.lower()
    point_in_country(latitude, longitude, country)


@app.command(name="country")
def country(country: str):
    country = country.lower()
    highlight_country(country)


if __name__ == "__main__":
    app()
