import logging
import time

import typer
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

from raspi_poe_mon import __title__, __version__
from raspi_poe_mon.poe_hat import PoeHat

logger = logging.getLogger('raspi_poe_mon')

app = typer.Typer(
    name='raspi_poe_mon',
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
    This is the entry point of your command line application. The values of the CLI params that
    are passed to this application will show up als parameters to this function.

    This docstring is where you describe what your command line application does.
    Try running `python -m raspi_poe_mon --help` to see how this shows up in the command line.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
    logger.info("Raspi PoE HAT Demo")

    poe_hat = PoeHat()
    poe_hat.fan_on()
    with poe_hat.draw() as draw:
        draw.rectangle(poe_hat.display.bounding_box, outline="white", fill="black")
        draw.text((10, 10), "Hello World", fill="white")
    time.sleep(1)
    poe_hat.fan_off()


def get_device() -> ssd1306:
    serial_display = i2c(port=1, address=0x3C)
    return ssd1306(serial_interface=serial_display, width=128, height=32)


if __name__ == "__main__":
    app()
