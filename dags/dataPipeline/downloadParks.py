"""
Downloads Parks boundary in Philly, and save it into the database.


"""
import geopandas as gpd

crs = 6564

park = gpd.read_file('https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson')
park = park.to_crs(crs)

parkUnion = gpd.GeoSeries(park.geometry.unary_union)