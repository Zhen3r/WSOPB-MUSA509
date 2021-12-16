import pandas as pd
import geopandas as gpd
import numpy as np
from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd
from shapely.geometry import Polygon


# load data from postgres
acsDataGeo = postgres_to_gpd("select * from acs_gpd;")
parkUnion = postgres_to_gpd("select st_union(geometry) geometry from park;")
cost = postgres_to_gpd('select * from cost')
flood = postgres_to_gpd('select * from flood').to_crs(4326)

city_boundary = gpd.GeoSeries(data=acsDataGeo.geometry.unary_union, crs=6564)

xmin, ymin, xmax, ymax = city_boundary.total_bounds
square_size = 300
cols = list(np.arange(xmin, xmax + square_size, square_size))
rows = list(np.arange(ymin, ymax + square_size, square_size))
polygons = []
for x in cols[:-1]:
    for y in rows[:-1]:
        polygons.append(Polygon(
            [(x, y), (x+square_size, y), (x+square_size, y+square_size), (x, y+square_size)]))


grid = gpd.GeoDataFrame({'geometry': polygons}, crs=6564)
grid = grid.sjoin(gpd.GeoDataFrame(
    geometry=city_boundary, crs=6564), how="left")
grid = grid[-grid.index_right.isna()]
grid = grid.to_crs(4326)
grid = grid[['geometry']].copy()

acsDataGeo["quanParkPct"] = acsDataGeo.parkPercentage.rank(pct=True)//0.2*0.25
acsDataGeo["race"] = 1 - (acsDataGeo.parkPercentage *
                          acsDataGeo["White"]).rank(pct=True)//0.2*0.25
acsDataGeo["income"] = 1 - (acsDataGeo.parkPercentage *
                            acsDataGeo["Median income"]).rank(pct=True)//0.2*0.25
acsDataGeo = acsDataGeo.to_crs(4326)

grid_joined = grid.sjoin(cost, how="left")[['geometry', 'score']].copy()
grid_joined = grid_joined.rename({'score': 'cost'}, axis=1)
grid_joined = grid_joined.sjoin(
    acsDataGeo[['geometry', 'race', 'income', 'quanParkPct']], how="left")
grid_joined = grid_joined.drop('index_right', axis=1)
grid_joined = grid_joined.sjoin(flood[['score', 'geometry']], how="left")
grid_joined = grid_joined.rename(
    {'score': 'flood', 'quanParkPct': 'park'}, axis=1)
grid_joined = grid_joined.drop('index_right', axis=1)
grid_joined = grid_joined.fillna(0)

gpd_to_postgres(grid_joined, "feasibility")
