"""
Transform land use data, calculate the average land value of each census tracts.
database table name: land_use
"""

import numpy as np
from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd
import pandas as pd

# load data from postgres
land_use = postgres_to_gpd("select * from raw_land_use;")
tracts = postgres_to_gpd("select * from tracts;")

# spatial join land_use and tracts
tracts_land_use = gpd.sjoin(land_use[["C_DIG1","geometry"]], tracts[["NAME10","geometry"]], op='within', how='left')

# set score for different category of land use: 1 - Residential - 1
#                                               2 - Commercial - 1
#                                               3 - Industrial - 1
#                                               4 - Civic/Institution - 1
#                                               5 - Transportation - 1
#                                               6 - Culture/Recreation - 0.75
#                                               7 - Park/Open Space - 0.25
#                                               8 - Water - 0.5
#                                               9 - Vacant or Other - 0.25
tracts_land_use["land_use_score"]=np.select([(tracts_land_use["C_DIG1"]==1),
                                             (tracts_land_use["C_DIG1"]==2),
                                             (tracts_land_use["C_DIG1"]==3),
                                             (tracts_land_use["C_DIG1"]==4),
                                             (tracts_land_use["C_DIG1"]==5),
                                             (tracts_land_use["C_DIG1"]==6),
                                             (tracts_land_use["C_DIG1"]==7),
                                             (tracts_land_use["C_DIG1"]==8),
                                             (tracts_land_use["C_DIG1"]==9)],
                                            [1,1,1,1,1,0.75,0.25,0.5,0.25])

# group by census tracts calculate average score of land use
tracts_land_use_group = tracts_land_use[['NAME10',"land_use_score"]].groupby(["NAME10"], as_index=False).mean()

# add geometry
tracts_land_use_group = pd.merge(tracts_land_use_group, tracts[["NAME10","geometry"]],on="NAME10")

# set dataframe to a geodataframe
tracts_land_use_group = gpd.GeoDataFrame(tracts_land_use_group)

# saving data to postgres
gpd_to_postgres(tracts_land_use_group, "land_use", if_exists="replace")
print("Success!")
