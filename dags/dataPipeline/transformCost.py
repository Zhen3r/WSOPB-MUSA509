"""
Calculate the score of cost of each census tracts.
database table name: cost
"""

import numpy as np
from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd

# load data from postgres
tracts_value_group = postgres_to_gpd("select * from land_value;")
tracts_building_group = postgres_to_gpd("select * from building_volume;")
tracts_land_use_group = postgres_to_gpd("select * from land_use;")

# normalize the land value
tracts_value_group["land_value_score"]=
(tracts_value_group["market_value"]-tracts_value_group["market_value"].min())/(tracts_value_group["market_value"].max()-tracts_value_group["market_value"].min())

# normalize the building volume
tracts_building_group["building_score"]=
(tracts_building_group["MAX_HGT"]-tracts_building_group["MAX_HGT"].min())/(tracts_building_group["MAX_HGT"].max()-tracts_building_group["MAX_HGT"].min())

# join land value and building volume
cost = pd.merge(tracts_value_group[["NAME10","geometry","land_value_score"]], tracts_building_group[["NAME10","geometry","building_score"]],on=["NAME10","geometry"])

# join land use
cost = pd.merge(cost, tracts_land_use_group,on=["NAME10","geometry"])

# calculate cost
cost["score"] = (cost["land_value_score"] + cost["building_score"] + cost["land_use_score"])/3

# saving data to postgres
gpd_to_postgres(cost, "cost", if_exists="replace")
print("Success!")
