# -*- coding: utf-8 -*-

"""Console script for model_builder."""
import sys
import click
import logging
from pathlib import Path

import hydroengine
from hydro_model_builder.model_builder import ModelBuilder

logger = logging.getLogger(__name__)


@click.group()
def main():
    return 0


builder = ModelBuilder()

template_names = [s.lower() for s in builder.get_generator_names()]


@click.command(name="generate-model")
@click.option("-o", "--options-file", required=True, help="Options file in YAML format")
@click.option("-r", "--results-dir", required=True, help="Result directory")
def generate_model(options_file, results_dir):
    # two YAML docs are expected in this file, one generic and one model specific
    dicts = builder.parse_config(options_file)
    genopt, modopt = dicts
    # TODO validate config
    # TODO fill in all defaults (for now we should supply all)
    msg = f"Going to create a '{genopt['model']}'/'{modopt['concept']}' model, it will be placed in '{results_dir}'"
    general_options(genopt)
    click.echo(msg)
    click.echo(builder.get_generator_names())


def get_hydro_data(region, ds):
    if ds["type"] == "raster" and ds["source"] == "earth-engine":
        # create directory
        Path(ds["path"]).parent.mkdir(parents=True, exist_ok=True)
        print("Downloading", ds["variable"])
        hydroengine.download_raster(
            region,
            ds["path"],
            ds["variable"],
            ds["cell_size"],
            ds["crs"],
            ds["region_filter"],
            ds["catchment_level"],
        )


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
