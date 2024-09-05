import pytest
from typer.testing import CliRunner

from raspi_poe_mon.main import app
from raspi_poe_mon.version import __version__

runner = CliRunner()


def test_main_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "raspi-poe-mon" in result.stdout


def test_main_help_short():
    result = runner.invoke(app, ["-h"])
    assert result.exit_code == 0
    assert "raspi-poe-mon" in result.stdout


def test_main_no_params():
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "raspi-poe-mon" in result.stdout


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


@pytest.mark.parametrize("command", ["clear", "fan", "run"])
def test_command_help(command: str):
    result = runner.invoke(app, [command, "--help"])
    assert result.exit_code == 0
    assert f"raspi-poe-mon {command}" in result.stdout
