"""
Generate the json file that the web uses.

1. equalityRace.geojson
variables: blockgroup race percentage
           blockgroup buffer park area percentage
           tract medium income
           GEOID
           geom

"""

import numpy as np
from ..utils.pipelineTools import postgres_to_gpd
import geopandas as gpd
from pathlib import Path

webResourcePath = Path(__file__).parents[2] / "html" / "res"
fileName = "resSection1.geojson"

sql = """
SELECT "GEOID" geoid,
    "White" pct_white,
    "Median income" medInc,
    "geometry" geometry,
    "parkPercentage" pct_park
from acs_gpd
"""

gdf = postgres_to_gpd(sql)
# project to 4326, which leatlet needs.
gdf = gdf.to_crs(4326)
gdf.to_file(webResourcePath/fileName, driver="GeoJSON")
