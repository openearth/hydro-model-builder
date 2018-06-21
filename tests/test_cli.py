from click.testing import CliRunner

from hydro_model_builder import cli

def test_cli_main():
    """Test the CLI."""
    runner = CliRunner()

    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'hydro_model_builder.cli.main' in result.output

    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

def test_cli_generate_model_help():
    """Show help for generate-model."""
    runner = CliRunner()

    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'hydro_model_builder.cli.main' in result.output

    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

