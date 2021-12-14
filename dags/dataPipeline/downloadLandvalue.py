"""
Downloads Land Value in Philly, and save it into the database.
database table name: raw_land_value
"""
import geopandas as gpd
from ..utils.pipelineTools import gpd_to_postgres

crs = 4326

land_value = gpd.read_file(
    'https://phl.carto.com/api/v2/sql?filename=opa_properties_public&format=geojson&skipfields=cartodb_id&q=SELECT+market_value,+the_geom+FROM+opa_properties_public')
land_value = land_value.to_crs(crs)
land_value = land_value.dropna()

gpd_to_postgres(land_value, "raw_land_value", if_exists="replace")

print("Success!")
