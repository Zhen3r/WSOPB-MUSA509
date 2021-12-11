"""
Find flood area that contain and don't contain parks and score them.
database table name: flood
"""

import numpy as np
from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd
import pandas as pd

# load data from postgres
flood100 = postgres_to_gpd("select * from flood100;")
flood500 = postgres_to_gpd("select * from flood500;")
park = postgres_to_gpd("select * from park;")
city_limits = postgres_to_gpd("select * from city_limits;")

# find the place in flood500 not in flood100
only500 = gpd.overlay(flood500, flood100, how='difference')

# find the place in flood500 only and don't contain parks
only500_nopark = gpd.overlay(only500, park, how='difference')

# find the place in flood500 only and contain parks
only500_park = gpd.overlay(only500, park, how='intersection')

# find the place both in flood100 and flood500 that don't contain parks
flood100_nopark = gpd.overlay(flood100, park, how='difference')

# find the place both in flood100 and flood500 that contain parks
flood100_park = gpd.overlay(flood100, park, how='intersection')

# find the place in Philly that will not be flood
total_flood = gpd.overlay(flood100, flood500, how='union')
noflood = gpd.overlay(city_limits, total_flood, how='difference')

# set flood score and description to all area
only500_nopark["score"]=0.5
only500_park["score"]=0
flood100_nopark["score"]=1
flood100_park["score"]=0
noflood["score"]=0

only500_nopark["description"]="500 year floodplain without parks"
only500_park["description"]="500 year floodplain within parks"
flood100_nopark["description"]="100 year floodplain without parks"
flood100_park["description"]="100 year floodplain within parks"
noflood["description"]="non-flood area"

# combine the areas together
flood = pd.concat([only500_nopark[["score","description","geometry"]], 
                   only500_park[["score","description","geometry"]], 
                   flood100_nopark[["score","description","geometry"]], 
                   flood100_park[["score","description","geometry"]], 
                   noflood[["score","description","geometry"]]]).reset_index(drop=True)

# saving data to postgres
gpd_to_postgres(flood, "flood", if_exists="replace")
print("Success!")
