# -*- coding: utf-8 -*-

"""Console script for hydro_model_builder."""
import sys
import click
import logging

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@click.command(name='generate-model')
@click.option('-t', '--template', required=True)
@click.option('-o', '--options-file', required=True)
@click.option('-r', '--results-dir', required=True)
def generate_model(template, options_file, results_dir):
    print(template)
    print(options_file)
    print(results_dir)
    click.echo('Generate model for a given region')


cli.add_command(generate_model)


# @click.command(name='upload-data')
# @click.option('-o', '--options', required=True)
# def upload():
#     click.echo('Upload model or data')
# cli.add_command(upload)


def main():
    cli()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
