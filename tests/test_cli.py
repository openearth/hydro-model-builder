import glob
import os
import sys
from click.testing import CliRunner

from hydro_model_builder import cli


def test_cli_main():
    """Test the CLI."""
    runner = CliRunner()

    result = runner.invoke(cli.main)
    assert result.exit_code == 0, "cli works"

    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Usage: " in help_result.output, "usage is shown"


def test_cli_generate_model_help():
    """Show help for generate-model."""
    runner = CliRunner()

    help_result = runner.invoke(cli.main, ["generate-model", "--help"])
    assert help_result.exit_code == 0
    assert "Usage: " in help_result.output
    assert "generate-model" in help_result.output


def test_cli_generate_model_template_contains():
    """Test if help message for templates contains list of templates"""
    prefix = (
        "model_generator_"
    )  # prefix for file names containing model generator templates
    suffix = ".py"  # suffix for file names containing model generator templates
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["generate-model", "--help"])

    # GD: kapote build
    # code_file = [s for s in sys.argv if 'cli.py' in s][0]
    # code_dir = os.path.split(code_file)[0]
    # model_build_template_fns = glob.glob(os.path.abspath(os.path.join(code_dir, '..', 'hydro_model_builder', '{:s}*{:s}'.format(prefix, suffix))))
    # models = [os.path.basename(fn).strip(prefix).strip(suffix) for fn in model_build_template_fns]
    # for n, model in enumerate(models):
    #    assert model in help_result.output.lower()  # check if the model is mentioned in the generate-model --help
