"""
Find flood area that contain and don't contain parks and score them.
database table name: flood
"""

from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd
import pandas as pd

print('starting...')
# load data from postgres
flood100 = postgres_to_gpd("select * from flood100;")
flood500 = postgres_to_gpd("select * from flood500;")
# park = postgres_to_gpd("select * from park;").to_crs(4326)
# city_limits = postgres_to_gpd("select * from city_limits;")

print('downloaded...')
# find the place in flood500 not in flood100
only500 = gpd.overlay(flood500, flood100, how='difference')

only500["score"] = 0.5
flood100["score"] = 1

print('overlayed...')
only500["description"] = "500 year floodplain"
flood100["description"] = "100 year floodplain"

# combine the areas together
flood = pd.concat([only500[["score", "description", "geometry"]],
                   flood100[["score", "description", "geometry"]]]).reset_index(drop=True)
flood = gpd.GeoDataFrame(flood)
flood["geometry"] = flood.to_crs(6564).simplify(1).to_crs(4326)
flood = flood.dissolve(by=['score', 'description']).reset_index()

print('uploading...')
# saving data to postgres
gpd_to_postgres(flood, "flood", if_exists="replace")
print("Success!")
