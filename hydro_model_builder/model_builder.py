import json
from pathlib import Path

import hydroengine
import numpy as np
import yaml
from shapely import geometry as sg

from hydro_model_builder import local_engine


def parse_config(configfile):
    with open(configfile) as f:
        return list(yaml.safe_load_all(f))


def get_paths(general_options):
    # TODO: use schema to validate here?
    d = {}
    if "hydro-engine" in general_options:
        for var in general_options["hydro-engine"]["datasets"]:
            d[var["variable"]] = var["path"]
    if "local" in general_options:
        for var in general_options["local"]["datasets"]:
            d[var["variable"]] = var["path"]
    return d


def load_region(region):
    if isinstance(region, dict): 
        pass
    else:
        with open(region) as f:
            region = json.load(f)
    assert (
        len(region["features"]) == 1
    ), "Region definition should contain only one feature."
    return region["features"][0]["geometry"]


def shapely_region(js):
    out = sg.shape(js)
    return out


def utm_epsg(region):
    """Return UTM EPSG code for a given region geojson feature"""

    centroid = sg.shape(region).centroid
    longitude, latitude = centroid.x, centroid.y

    # northern latitudes
    if latitude > 0:
        UTMzone = int((np.floor((longitude + 180.0) / 6.0) % 60.0) + 1)
        epsg = 32600 + UTMzone
    # southern latitudes
    else:
        UTMzone = int((np.floor((longitude + 180.0) / 6.0) % 60.0) + 1)
        epsg = 32700 + UTMzone

    return epsg


def get_hydro_data(region, ds):
    if ds["function"] == "get-raster":
        # create directory
        Path(ds["path"]).parent.mkdir(parents=True, exist_ok=True)
        if ds["crs"].lower() == "utm":
            ds["crs"] = f"EPSG:{utm_epsg(shapely_region(region))}"
        hydroengine.download_raster(
            region,
            ds["path"],
            ds["variable"],
            ds["cell_size"],
            ds["crs"],
            ds["region_filter"],
            ds["catchment_level"],
        )
    elif ds["function"] == "get-catchments":
        hydroengine.download_catchments(
            region, ds["path"], ds["region_filter"], ds["catchment_level"]
        )
    elif ds["function"] == "get-rivers":
        filter_upstream_gt = 1000
        hydroengine.download_rivers(
            region,
            ds["path"],
            filter_upstream_gt,
            ds["region_filter"],
            ds["catchment_level"],
        )
    else:
        raise ValueError(f"Invalid function provided for {ds['variable']}.")


def get_local_data(meta, ds):
    # get data from local sources one by one
    if ds["function"] == "get-raster":
        local_engine.get_raster(ds["source"], ds["path"], **meta["raster"])
    elif ds["function"] == "get-features":
        local_engine.get_features(ds["source"], ds["path"], **meta["features"])
    else:
        raise ValueError(f"Invalid function for {ds['variable']}.")


def general_options(d):
    # get data from hydro-engine one by one
    d["region"] = load_region(d["region"])

    if "hydro-engine" in d:
        defaults = d["hydro-engine"]["defaults"]
        for ds_override in d["hydro-engine"]["datasets"]:
            ds = defaults.copy()
            ds.update(ds_override)
            get_hydro_data(d["region"], ds)

    if "local" in d:
        # metadata of destination is similar every time
        # so we can precompute it
        region = shapely_region(d["region"])
        crs = d["local"]["defaults"]["crs"]
        if crs.lower() == "utm":
            crs = f"EPSG:{utm_epsg(region)}"
        cellsize = d["local"]["defaults"]["cell_size"]

        meta = local_engine.spatial_meta(region, crs, cellsize)
        defaults = d["local"]["defaults"]
        for ds_override in d["local"]["datasets"]:
            ds = defaults.copy()
            ds.update(ds_override)
            get_local_data(meta, ds)
