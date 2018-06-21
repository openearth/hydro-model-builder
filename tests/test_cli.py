from click.testing import CliRunner

from hydro_model_builder import cli


def test_cli_main():
    """Test the CLI."""
    runner = CliRunner()

    result = runner.invoke(cli.main)
    assert result.exit_code == 0, "cli works"

    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Usage: ' in help_result.output, "usage is shown"


def test_cli_generate_model_help():
    """Show help for generate-model."""
    runner = CliRunner()

    help_result = runner.invoke(cli.main, ['generate-model', '--help'])
    assert help_result.exit_code == 0
    assert 'Usage: ' in help_result.output
    assert 'generate-model' in help_result.output


def test_cli_generate_model_template_contains():
    """Test if help message for templates contains list of templates"""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['generate-model', '--help'])
    assert 'wflow' in help_result.output.lower()
    assert 'imod' in help_result.output.lower()
