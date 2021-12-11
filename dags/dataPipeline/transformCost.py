"""
Calculate the score of cost of each census tracts.
database table name: cost
"""

import numpy as np
from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd
import pandas as pd

# load data from postgres
tracts_value_group = postgres_to_gpd("select * from land_value;")
tracts_building_group = postgres_to_gpd("select * from building_volume;")
tracts_land_use_group = postgres_to_gpd("select * from land_use;")

# set score for land value
tracts_value_group["land_value_score"]=np.select([(tracts_value_group["market_value"]<103718.04),
                                                  (tracts_value_group["market_value"].between(103718.04, 166669.01)),
                                                  (tracts_value_group["market_value"].between(166669.01, 265005.29)),
                                                  (tracts_value_group["market_value"].between(265005.29, 481603.59)),
                                                  (tracts_value_group["market_value"]>481603.59)],
                                                 [0,0.25,0.5,0.75,1])

# set score for building volume
tracts_building_group["building_score"]=np.select([(tracts_building_group["MAX_HGT"]<28.27),
                                                  (tracts_building_group["MAX_HGT"].between(28.27, 29.95)),
                                                  (tracts_building_group["MAX_HGT"].between(29.95, 31.49)),
                                                  (tracts_building_group["MAX_HGT"].between(31.49, 33.88)),
                                                  (tracts_building_group["MAX_HGT"]>33.88)],
                                                 [0,0.25,0.5,0.75,1])

# join land value and building volume
cost = pd.merge(tracts_value_group[["NAME10","geometry","land_value_score"]], tracts_building_group[["NAME10","geometry","building_score"]],on=["NAME10","geometry"])

# join land use
cost = pd.merge(cost, tracts_land_use_group,on=["NAME10","geometry"])

# calculate cost
cost["score"] = (cost["land_value_score"] + cost["building_score"] + cost["land_use_score"])/3

# saving data to postgres
gpd_to_postgres(cost, "cost", if_exists="replace")
print("Success!")
