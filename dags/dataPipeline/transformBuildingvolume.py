"""
Transform building volume data, calculate the average building volume of each census tracts.
database table name: building_volume
"""

from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd
import pandas as pd

# load data from postgres
building = postgres_to_gpd("select * from raw_building_volume;")
tracts = postgres_to_gpd("select * from tracts;")

print('downloaded')
# spatial join building and tracts
tracts_building = gpd.sjoin(building[["MAX_HGT", "geometry"]], tracts[[
                            "NAME10", "geometry"]], op='within', how='left')

# group by census tracts calculate average building volume
tracts_building_group = tracts_building.drop(
    ['geometry', "index_right"], axis=1).groupby(["NAME10"], as_index=False).mean()

# add geometry
tracts_building_group = pd.merge(
    tracts_building_group, tracts[["NAME10", "geometry"]], on="NAME10")

# set dataframe to a geodataframe
tracts_building_group = gpd.GeoDataFrame(tracts_building_group)

# saving data to postgres
gpd_to_postgres(tracts_building_group, "building_volume", if_exists="replace")
print("Success!")
