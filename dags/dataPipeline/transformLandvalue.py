"""
Transform land value data, calculate the average land value of each census tracts.
database table name: land_value
"""

from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd
import pandas as pd

# load data from postgres
land_value = postgres_to_gpd("select * from raw_land_value;")
tracts = postgres_to_gpd("select * from tracts;")

# spatial join land_value and tracts
tracts_value = gpd.sjoin(land_value[["market_value", "geometry"]], tracts[[
                         "NAME10", "geometry"]], op='within', how='left')

# group by census tracts calculate average land value
tracts_value_group = tracts_value[["NAME10", "market_value"]].groupby(
    ["NAME10"], as_index=False).mean()

# add geometry
tracts_value_group = pd.merge(
    tracts_value_group, tracts[["NAME10", "geometry"]], on="NAME10")

# set dataframe to a geodataframe
tracts_value_group = gpd.GeoDataFrame(tracts_value_group)

# saving data to postgres
gpd_to_postgres(tracts_value_group, "land_value", if_exists="replace")
print("Success!")
