"""
Downloads flood data in Philly, and save it into the database.
database table name: flood
"""

import geopandas as gpd
from ..utils.pipelineTools import gpd_to_postgres

crs = 4326

flood = gpd.read_file(
    'https://opendata.arcgis.com/datasets/1d6d353ab50b4884b586c05ee2a661db_0.geojson')
flood = park.to_crs(crs)
gpd_to_postgres(flood, "flood", if_exists="replace")

print("Success!")
