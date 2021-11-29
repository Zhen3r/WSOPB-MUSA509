"""
Downloads ACS data and its geometry in Philly, and save it into the database.
database table name: raw_acs_gpd
"""

import cenpy
from ..utils.pipelineTools import gpd_to_postgres

acsVarDict = {
    'B02001_001E': 'Total population',
    'B02001_002E': 'White',
    'B02001_003E': 'Black or African American',
    'B02001_004E': 'American Indian and Alaska Native',
    'B02001_005E': 'Asian',
    'B02001_006E': 'Native Hawaiian and Other Pacific Islander',
    'B06011_001E': 'Median income'}
acsVars = ["NAME"]+list(acsVarDict.keys())

crs = 6564

conn = cenpy.remote.APIConnection("ACSDT5Y2019")
acsDataBlockGroup = conn.query(acsVars, geo_unit='block group', geo_filter={
                               "state": "42", "county": "101"})

# income is only available in tracts level, so tract level is also necessary.
acsDataTract = conn.query(acsVars, geo_unit='tract', geo_filter={
                          "state": "42", "county": "101"})

# merge tract level and bg level data
acsData = acsDataTract[["B06011_001E", "tract"]].merge(
    acsDataBlockGroup.drop("B06011_001E", axis=1), how="left", on="tract")

# download acs blockgroup geometry
conn.set_mapservice("tigerWMS_ACS2019")
whereClause = "STATE = 42 AND COUNTY = 101"
phillyGeo = conn.mapservice.layers[10].query(where=whereClause)

# merge dataframe and geometry
acsDataGeo = (phillyGeo
              .merge(acsData,
                     left_on=["STATE", "COUNTY", "TRACT", "BLKGRP"],
                     right_on=["state", "county", "tract", "block group"],)
              .rename(acsVarDict, axis=1)
              .to_crs(crs))

# save it to postgres
gpd_to_postgres(acsDataGeo, "raw_acs_gpd", if_exists="replace")
print("Success!")
