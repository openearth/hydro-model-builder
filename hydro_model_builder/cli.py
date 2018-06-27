# -*- coding: utf-8 -*-

"""Console script for model_builder."""
import sys
import click
import logging

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
    print(options_file)
    print(results_dir)
    click.echo("Generate model for a given region")


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
