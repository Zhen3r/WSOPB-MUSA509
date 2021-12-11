"""
Downloads 100 Year Floodplain data in Philly, and save it into the database.
database table name: flood100
"""

import geopandas as gpd
from ..utils.pipelineTools import gpd_to_postgres

crs = 4326

flood100 = gpd.read_file(
    'https://opendata.arcgis.com/datasets/1d6d353ab50b4884b586c05ee2a661db_0.geojson')
flood100 = flood100.to_crs(crs)
gpd_to_postgres(flood100, "flood100", if_exists="replace")

flood500 = gpd.read_file(
    'https://opendata.arcgis.com/datasets/1e6f6315225544c88549478d25cc5181_0.geojson')
flood500 = flood500.to_crs(crs)
gpd_to_postgres(flood500, "flood500", if_exists="replace")


print("Success!")
