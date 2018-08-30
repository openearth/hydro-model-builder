# -*- coding: utf-8 -*-

"""Console script for model_builder."""
import sys
import click
import logging
from pathlib import Path
from shapely import geometry as sg
import hydroengine
import numpy as np
from hydro_model_builder.model_builder import ModelBuilder
from hydro_model_generator_wflow import ModelGeneratorWflow

logger = logging.getLogger(__name__)


@click.group()
def main():
    return 0


builder = ModelBuilder()

template_names = [s.lower() for s in builder.get_generator_names()]

@click.command(name="generate-model")
@click.option("-o", "--options-file", required=True, help="Options file in YAML format")
@click.option("-r", "--results-dir", required=True, help="Result directory")
@click.option('--skip-download/--no-skip-download', default=False, help="Skip downloading data if already done")
def generate_model(options_file, results_dir, skip_download):
    # two YAML docs are expected in this file, one generic and one model specific
    dicts = builder.parse_config(options_file)
    genopt, modopt = dicts
    # TODO validate config
    # TODO fill in all defaults (for now we should supply all)
    msg = f"Going to create a '{genopt['model']}'/'{modopt['concept']}' model, it will be placed in '{results_dir}'"
    print(msg)
    if not skip_download:
        general_options(genopt)
    if genopt['model'] == 'wflow':
        genwf = ModelGeneratorWflow()
        genwf.generate_model(genopt, modopt)



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
    if ds["function"] == "get-raster" and ds["source"] == "earth-engine":
        # create directory
        Path(ds["path"]).parent.mkdir(parents=True, exist_ok=True)
        if ds["crs"].lower() == "utm":
            ds["crs"] = f"EPSG:{utm_epsg(region)}"
        hydroengine.download_raster(
            region,
            ds["path"],
            ds["variable"],
            ds["cell_size"],
            ds["crs"],
            ds["region_filter"],
            ds["catchment_level"],
        )
    elif ds["function"] == "get-catchments" and ds["source"] == "earth-engine":
        hydroengine.download_catchments(region, ds["path"], ds["region_filter"], ds["catchment_level"])
    elif ds["function"] == "get-rivers" and ds["source"] == "earth-engine":
        filter_upstream_gt = 1000
        hydroengine.download_rivers(region, ds["path"], filter_upstream_gt, ds["region_filter"], ds["catchment_level"])



def general_options(d):
    # get data from hydro-engine one by one
    defaults = d["hydro-engine"]["defaults"]
    for ds_override in d["hydro-engine"]["datasets"]:
        ds = defaults.copy()
        ds.update(ds_override)
        if ds["source"] == "earth-engine":
            get_hydro_data(d["region"], ds)
        else:
            # TODO support non earth-engine datasets
            print("skipped variable:", ds["variable"])


main.add_command(generate_model)

# @click.command(name='upload-data')
# @click.option('-o', '--options', required=True)
# def upload():
#     click.echo('Upload model or data')
# cli.add_command(upload)


if __name__ == "__main__":
    # use sys.argv[1:] to allow using PyCharm debugger
    # https://github.com/pallets/click/issues/536
    main(sys.argv[1:])  # pragma: no cover
