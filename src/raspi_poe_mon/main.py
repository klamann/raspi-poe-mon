import logging

import typer

from raspi_poe_mon import __title__, __version__
from raspi_poe_mon.ctrl import Controller

logger = logging.getLogger('raspi_poe_mon')

app = typer.Typer(
    name='raspi-poe-mon',
    help="A controller for the display and fan of the Raspi PoE HAT (Type B)"
)


def version_callback(version: bool):
    if version:
        typer.echo(f"{__title__} {__version__}")
        raise typer.Exit()


ConfigOption = typer.Option(
    None, '-c', '--config', metavar='PATH', help="path to the program configuration")
VersionOption = typer.Option(
    None, '-v', '--version', callback=version_callback, is_eager=True,
    help="print the program version and exit")


@app.command()
def main(
    config_file: str = ConfigOption,
    version: bool = VersionOption,
    fan_on_temp: float = 50,
    fan_off_temp: float = 45,
    frame_time: float = 2.0
):
    """
    a controller for the display and fan of the Raspberry Pi Power Over Ethernet HAT (Type B),
    compatible with Raspberry Pi 3B+/4B.
    """
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s]: %(message)s")
    logger.info("Starting Raspi PoE HAT Monitor")
    ctrl = Controller(fan_on_temp=fan_on_temp, fan_off_temp=fan_off_temp, frame_time=frame_time)
    ctrl.main_loop()


if __name__ == "__main__":
    app()
