from typing import Optional

import typer

from point_in_country import point_in_country

app = typer.Typer()


@app.command(name="point")
def point(
    latitude: float,
    longitude: float,
    country: Optional[str] = "Southeast Asia",
):
    point_in_country(latitude, longitude, country)


if __name__ == "__main__":
    app()
