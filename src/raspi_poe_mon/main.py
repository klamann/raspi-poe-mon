import logging
import time

import typer

from raspi_poe_mon import __title__, __version__
from raspi_poe_mon.ip import IpDisplay
from raspi_poe_mon.poe_hat import PoeHat

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
def main(config_file: str = ConfigOption, version: bool = VersionOption):
    """
    a controller for the display and fan of the Raspberry Pi Power Over Ethernet HAT (Type B),
    compatible with Raspberry Pi 3B+/4B.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
    logger.info("Raspi PoE HAT Demo")

    poe_hat = PoeHat()
    # poe_hat.fan_on()

    display = IpDisplay(poe_hat)
    display.draw_frame()

    time.sleep(10)
    poe_hat.fan_off()


if __name__ == "__main__":
    app()
