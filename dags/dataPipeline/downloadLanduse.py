"""
Downloads Land Use in Philly, and save it into the database.
database table name: raw_land_use
"""
import geopandas as gpd
from ..utils.pipelineTools import gpd_to_postgres

crs = 4326

land_use = gpd.read_file(
    'https://www.pasda.psu.edu/download/philacity/data/historic/LandUse/PhiladelphiaLandUse2016.zip')
land_use = land_use.to_crs(crs)
gpd_to_postgres(land_use, "raw_land_use", if_exists="replace")

print("Success!")
