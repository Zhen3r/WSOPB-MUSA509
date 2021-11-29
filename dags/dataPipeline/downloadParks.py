"""
Downloads Parks boundary in Philly, and save it into the database.
database table name: park
"""
import geopandas as gpd
from ..utils.pipelineTools import gpd_to_postgres

crs = 6564

park = gpd.read_file(
    'https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson')
park = park.to_crs(crs)
gpd_to_postgres(park, "park", if_exists="replace")

# don't need to union it, can be done with sql
# parkUnion = gpd.GeoSeries(park.geometry.unary_union)

print("Success!")
