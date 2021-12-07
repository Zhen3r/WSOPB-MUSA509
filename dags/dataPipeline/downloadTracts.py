"""
Downloads Census Tracts in Philly, and save it into the database.
database table name: tracts
"""
import geopandas as gpd
from ..utils.pipelineTools import gpd_to_postgres

crs = 4326

tracts = gpd.read_file(
    'https://opendata.arcgis.com/datasets/8bc0786524a4486bb3cf0f9862ad0fbf_0.geojson')
tracts = tracts.to_crs(crs)
gpd_to_postgres(tracts, "tracts", if_exists="replace")

print("Success!")
