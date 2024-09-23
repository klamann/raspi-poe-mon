import pytest
from click.testing import Result
from typer.testing import CliRunner

from raspi_poe_mon import main
from raspi_poe_mon.main import app
from raspi_poe_mon.version import __version__

runner = CliRunner()


def test_main_help():
    result = runner.invoke(app, ["--help"])
    validate_help(result, "raspi-poe-mon")


def test_main_help_short():
    result = runner.invoke(app, ["-h"])
    validate_help(result, "raspi-poe-mon")


def test_main_no_params():
    result = runner.invoke(app, [])
    validate_help(result, "raspi-poe-mon")


def test_version():
    result = runner.invoke(app, ["--version"])
    validate_help(result, __version__)


@pytest.mark.parametrize("command", ["display", "fan", "run"])
def test_command_help(command: str):
    result = runner.invoke(app, [command, "--help"])
    validate_help(result, f"raspi-poe-mon {command}")


def validate_help(result: Result, contains: str):
    assert result.exit_code == 0
    assert contains in result.stdout
    print(result.stdout)


@pytest.mark.timeout(2)
def test_dry_run():
    main.run(dry_run=True, verbose=True, frame_time=0.02, timeout=0.05)


@pytest.mark.timeout(2)
def test_profiling():
    main.run(dry_run=True, profiling=True, frame_time=0.05, timeout=0.1)
