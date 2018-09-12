from affine import Affine
from functools import partial
import json
import numpy as np
from pathlib import Path
import pyproj
import os
import rasterio
import shapely.ops
import shapely.geometry as sg
import shutil
import subprocess
import xarray as xr


def region_features(region_path):
    with open(region_path) as f:
        js = json.load(f)
    features = [sg.shape(f["geometry"]) for f in js["features"]]
    return sg.MultiPolygon(features)


def reproject(shapes, src_proj, dst_proj):
    project = partial(pyproj.transform, src_proj, dst_proj)
    return shapely.ops.transform(project, shapes)


def round_extent(extent, cellsize):
    """Increases the extent until all sides lie on a coordinate
    divisible by cellsize."""
    xmin, ymin, xmax, ymax = extent
    xmin = np.floor(xmin / cellsize) * cellsize
    ymin = np.floor(ymin / cellsize) * cellsize
    xmax = np.ceil(xmax / cellsize) * cellsize
    ymax = np.ceil(ymax / cellsize) * cellsize
    return xmin, ymin, xmax, ymax


def get_raster(src_path, dst_transform, nrow, ncol, dst_crs, dst_path):
    with rasterio.open(src_path) as src:
        kwargs = src.meta.copy()
        kwargs.update(
            {"crs": dst_crs, "transform": dst_transform, "width": ncol, "heigth": nrow}
        )

        with rasterio.open(dst_path, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                rasterio.warp.reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=dst_transform,
                    dst_crs=dst_crs,
                    resampling=rasterio.warp.Resampling.nearest,
                )


def get_features(source, path, crs, bounds):
    src_proj = pyproj.Proj(init="EPSG:4326")
    dst_proj = pyproj.Proj(f"init={crs}")
    xmin, ymin, xmax, ymax = bounds
    x = np.array([xmin, xmin, xmax, xmax])
    y = np.array([ymin, ymax, ymin, ymax])
    # project the other way around to get all data within the reprojected box
    lon, lat = pyproj.transform(dst_proj, src_proj)
    # clip
    # ogr2ogr -f "ESRI Shapefile" output.shp input.shp -clipsrc <x_min> <y_min> <x_max> <y_max>
    subprocess.call(f"ogr2ogr -f ESRI Shapefile {path} {source} -clipsrc {min(lon)} {max(lon)} {min(lat)} {max{lat}}")
    # reproject
    # this won't work, we'll have to produce a temporary file
    # ogr2ogr output.shp -t_srs "EPSG:4326" input.shp
    subprocess.call(f'ogr2ogr {path} -t_srs "{crs}" {source}')
    # maybe (re)creating a spatial index is a good idea?
    # ogrinfo example.shp -sql "CREATE SPATIAL INDEX ON example"


def get_data(region, path, source, cellsize, crs):
    src_proj = pyproj.Proj(init="EPSG:4326")
    dst_proj = pyproj.Proj(f"init={crs}")
    reprojected_region = reproject(region, src_proj, dst_proj)
    xmin, ymin, xmax, ymax = round_extent(reprojected_region.bounds, cellsize)
    nrow = int((ymax - ymin) / cellsize) - 1
    ncol = int((xmax - xmin) / cellsize) - 1
    dst_transform = Affine(cellsize, 0.0, xmin, 0.0, -cellsize, ymax)
    reproject_raster(source, dst_transform, nrow, ncol, crs, path)
