"""
Make buffers of Parks, 250m, 500m, 750m.
database table name: park_buffer250, park_buffer500, park_buffer750
"""

import numpy as np
from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd

# load data from postgres
parkUnion = postgres_to_gpd("select st_union(geometry) geometry from park;")

# create buffer
buffer250 = park.geometry.buffer(250)
buffer500 = park.geometry.buffer(500)
buffer750 = park.geometry.buffer(750)

# Union buffer
bufferUnion250 = gpd.GeoSeries(buffer250.geometry.unary_union)
bufferUnion750 = gpd.GeoSeries(buffer750.geometry.unary_union)
bufferUnion500 = gpd.GeoSeries(buffer500.geometry.unary_union)

# saving data to postgres
gpd_to_postgres(bufferUnion250, "park_buffer250", if_exists="replace")
gpd_to_postgres(bufferUnion750, "park_buffer750", if_exists="replace")
gpd_to_postgres(bufferUnion500, "park_buffer500", if_exists="replace")
print("Success!")
