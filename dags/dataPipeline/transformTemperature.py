"""
Transform the crs of Landsat data, calculate the temperature in Fahrenheit.
database table name: 
"""

import numpy as np
from ..utils.pipelineTools import postgres_to_gpd, gpd_to_postgres
import geopandas as gpd
import rasterio as rio
from rasterio.mask import mask
from rasterio import crs
from rasterio.warp import calculate_default_transform, reproject, Resampling

final_crs = crs.CRS.from_epsg('4326')

in_path = './data/LC08_L2SP_014032_20210927_20211001_02_T1_ST_B10.TIF'
out_path = './data/reproject.tif'

# reproject to 4326


def reproject_raster(in_path, out_path):
    # reproject raster to project crs
    with rio.open(in_path) as src:
        src_crs = src.crs
        transform, width, height = calculate_default_transform(
            src_crs, final_crs, src.width, src.height, *src.bounds)
        profile = src.meta.copy()

        profile.update({
            'crs': final_crs,
            'transform': transform,
            'width': width,
            'height': height})

        with rio.open(out_path, 'w', **profile) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rio.band(src, i),
                    destination=rio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=final_crs,
                    resampling=Resampling.nearest)
    return(out_path)


reproject_raster(in_path, out_path)

# open reprojected tiff and city limit
f = rio.open(out_path)
city_limits = postgres_to_gpd('select * from city_limits;')

city_limits = city_limits.to_crs(f.crs.data['init'])

# create mask
masked_city, mask_transform = mask(
    dataset=f,
    shapes=city_limits.geometry,
    crop=True,
    all_touched=True,
    filled=False,
)

# get raw temperature of Philly
temperature = masked_city[0]
temperature

# calculate temperature in Fahrenheit


def calculate_temperature(data):
    """
    Calculate the Fahrenheit from temparature tiff
    """
    # Convert to floats
    data = data.astype(float)
    # Get valid entries
    check = data.mask == False
    # Where the check is True, return the NDVI, else return NaN
    temperature = np.where(
        check,  1.8 * ((data * 0.00341802 + 149.0) - 273) + 32, np.nan)
    return temperature


temperature = calculate_temperature(temperature)

# init output profile
profile = f.profile

# output bounds
landsat_extent = [
    city_limits.total_bounds[0],
    city_limits.total_bounds[1],
    city_limits.total_bounds[2],
    city_limits.total_bounds[3],
]

# calculate output transform
transform, width, height = calculate_default_transform(
    f.crs, final_crs, temperature.shape[1], temperature.shape[0], *landsat_extent)

# update profile
profile.update(
    width=width,
    height=height,
    transform=transform
)

# save temperaure tiff to local
with rio.open('./data/temperature.tif', 'w', **profile) as dst:
    dst.write(temperature, 1)

print("Success!")
