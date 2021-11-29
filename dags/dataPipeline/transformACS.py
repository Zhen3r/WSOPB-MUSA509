"""
Transform acs data, calculate the park area and pct.
database table name: acs_gpd
"""

import numpy as np
from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd
# from math import log

# load data from postgres
acsDataGeo = postgres_to_gpd("select * from raw_acs_gpd;")
parkUnion = postgres_to_gpd("select st_union(geometry) geometry from park;")

# select useful col
acsColList = ["GEOID", 'Total population',
              'White', 'Median income', "geometry"]
acsDataGeo = acsDataGeo[acsColList].copy()
acsDataGeo[acsColList[:-1]] = acsDataGeo[acsColList[:-1]].astype("int")

# Dividing Race into White and non-White, because other race like Asian
# has small population.
acsDataGeo["White"] = acsDataGeo["White"] / acsDataGeo["Total population"]
acsDataGeo["Non-White"] = 1 - acsDataGeo["White"]

# There is some missing data in DF
acsDataGeo = acsDataGeo.fillna(0)

# The income of some tracts is -66666666
acsDataGeo.loc[acsDataGeo["Median income"] < 0, 'Median income'] = np.nan

# calculate park area within distance
searchDistance = 500  # (m)


def getParkAreaWithinDistance(acsblockgroups: gpd.GeoDataFrame, distance: float, park: gpd.GeoDataFrame):
    buffer = acsblockgroups.geometry.buffer(distance)
    area = park.intersection(buffer).area
    return(area.squeeze())


acsDataGeo["parkArea"] = acsDataGeo.apply(getParkAreaWithinDistance, axis=1,
                                          distance=searchDistance, park=parkUnion)
acsDataGeo['parkPercentage'] = acsDataGeo["parkArea"] / \
    acsDataGeo.geometry.area

# saving data to postgres
gpd_to_postgres(acsDataGeo, "acs_gpd", if_exists="replace")
print("Success!")
