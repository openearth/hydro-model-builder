# -*- coding: utf-8 -*-

"""Console script for hydro_model_builder."""
import sys
import click
import logging

logger = logging.getLogger(__name__)


@click.group()
def main():
    return 0

@click.command(name='generate-model')
@click.option('-t', '--template', required=True, help='Model template iMOD/wflow')
@click.option('-o', '--options-file', required=True, help='Options file in YAML format')
@click.option('-r', '--results-dir', required=True, help='Result directory')

def generate_model(template, options_file, results_dir):
    print(template)
    print(options_file)
    print(results_dir)
    click.echo('Generate model for a given region')


main.add_command(generate_model)


# @click.command(name='upload-data')
# @click.option('-o', '--options', required=True)
# def upload():
#     click.echo('Upload model or data')
# cli.add_command(upload)




if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
