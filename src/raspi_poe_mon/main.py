import logging
import time

import typer

from raspi_poe_mon import __title__, __version__
from raspi_poe_mon.ip import IpDisplay
from raspi_poe_mon.poe_hat import PoeHat
from raspi_poe_mon import util

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
    fps=1.0
):
    """
    a controller for the display and fan of the Raspberry Pi Power Over Ethernet HAT (Type B),
    compatible with Raspberry Pi 3B+/4B.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
    logger.info("Starting Raspi PoE HAT Monitor")
    poe_hat = PoeHat()
    display = IpDisplay(poe_hat)
    try:
        while True:
            temp = util.get_cpu_temp()
            if not poe_hat.is_fan_on() and temp > fan_on_temp:
                logger.info(f"CPU temperature at {temp}, turning fan ON")
                poe_hat.fan_on()
            elif poe_hat.is_fan_on() and temp < fan_off_temp:
                logger.info(f"CPU temperature at {temp}, turning fan OFF")
                poe_hat.fan_off()
            display.draw_frame()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        poe_hat.cleanup()


if __name__ == "__main__":
    app()
