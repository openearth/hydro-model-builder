from affine import Affine
from functools import partial
import numpy as np
from pathlib import Path
import pyproj
import rasterio
import rasterio.warp
import shapely.geometry as sg
import shapely.ops
import shlex
from subprocess import Popen, PIPE


def reproject_features(shapes, src_proj, dst_proj):
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


def spatial_meta(region, crs, cellsize):
    src_proj = pyproj.Proj(init="EPSG:4326")
    dst_proj = pyproj.Proj(init=f"{crs}")
    reprojected = reproject_features(sg.shape(region), src_proj, dst_proj)

    bounds = round_extent(reprojected.bounds, cellsize)
    xmin, ymin, xmax, ymax = bounds
    nrow = int((ymax - ymin) / cellsize) - 1
    ncol = int((xmax - xmin) / cellsize) - 1

    x = np.array([xmin, xmin, xmax, xmax])
    y = np.array([ymin, ymax, ymin, ymax])
    lon, lat = pyproj.transform(dst_proj, src_proj, x, y)
    latlon_bounds = min(lon), min(lat), max(lon), max(lat)

    raster_meta = {
        "transform": Affine(cellsize, 0.0, xmin, 0.0, -cellsize, ymax),
        "crs": crs,  ## crs string, e.g. "EPSG:4326"
        "nrow": nrow,
        "ncol": ncol,
    }

    features_meta = {
        "crs": crs,  # crs string, e.g. "EPSG:4326"
        "bounds": latlon_bounds,
    }

    d = {"raster": raster_meta, "features": features_meta}

    return d


def get_raster(source, path, crs, transform, nrow, ncol):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(source) as src:
        kwargs = src.meta.copy()
        kwargs.update(
            {"crs": crs, "transform": transform, "width": ncol, "height": nrow}
        )

        print(f"Clipping and reprojecting {source}")
        with rasterio.open(path, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                rasterio.warp.reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=crs,
                    resampling=rasterio.warp.Resampling.nearest,
                )


def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    # from https://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    return exitcode, out, err


def get_features(source, path, crs, bounds):
    # TODO: empty geometries create problems later on
    # maybe also do: ogr2ogr -f "ESRI Shapefile" -dialect sqlite -sql "select * from input where geometry is not null" output.shp input.shp
    # maybe (re)creating a spatial index is a good idea?
    # ogrinfo example.shp -sql "CREATE SPATIAL INDEX ON example"
    xmin, ymin, xmax, ymax = bounds
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    cmd = f'ogr2ogr -f "ESRI Shapefile" -clipsrc {xmin} {ymin} {xmax} {ymax} {path} {source} -t_srs {crs}'
    print(f'Clipping and reprojecting {source}')
    exitcode, _, err = get_exitcode_stdout_stderr(cmd)
    if exitcode != 0:
        raise RuntimeError(
            f"An error occurred clipping and reprojecting {source}\n"
            f"During execution of:\n"
            f"{cmd}\n"
            f"\n"
            f"Error message:\n"
            f"{err.decode()}"
            )
