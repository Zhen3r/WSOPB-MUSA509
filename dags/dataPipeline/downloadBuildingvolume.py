"""
Downloads Building Volume in Philly, and save it into the database.
database table name: raw_building_volume
"""
import geopandas as gpd
from ..utils.pipelineTools import gpd_to_postgres

crs = 4326

building = gpd.read_file(
    'https://opendata.arcgis.com/datasets/ab9e89e1273f445bb265846c90b38a96_0.geojson')
building = building.to_crs(crs)
gpd_to_postgres(building, "raw_building_volume", if_exists="replace")

print("Success!")
