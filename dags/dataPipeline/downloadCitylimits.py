"""
Downloads the city limit of Philly, and save it into the database.
database table name: city_limits
"""

import geopandas as gpd
from ..utils.pipelineTools import gpd_to_postgres

crs = 4326

city_limits = gpd.read_file(
    'http://data.phl.opendata.arcgis.com/datasets/405ec3da942d4e20869d4e1449a2be48_0.geojson')
city_limits = city_limits.to_crs(crs)
gpd_to_postgres(city_limits, "city_limits", if_exists="replace")

print("Success!")
