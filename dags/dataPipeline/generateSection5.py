"""
Generate the json file that the web uses.

1. heat.geojson
variables: geometry

"""

from ..utils.pipelineTools import postgres_to_gpd
from pathlib import Path

webResourcePath = Path(__file__).parents[2] / "html" / "res"
fileName = "heat.geojson"

sql = "select * from urban_heat_island"

gdf = postgres_to_gpd(sql)
# project to 4326, which leatlet needs.
# gdf = gdf.to_crs(4326)
gdf.to_file(webResourcePath/fileName, driver="GeoJSON")
