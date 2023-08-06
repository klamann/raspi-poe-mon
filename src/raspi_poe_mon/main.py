import logging
from enum import Enum

import typer

from raspi_poe_mon import __title__, __version__
from raspi_poe_mon.ctrl import Controller
from raspi_poe_mon.poe_hat import PoeHat

logger = logging.getLogger('raspi_poe_mon')
app = typer.Typer(name='raspi-poe-mon')


def version_callback(version: bool):
    if version:
        typer.echo(f"{__title__} {__version__}")
        raise typer.Exit()


VersionOption = typer.Option(
    None, '-v', '--version', callback=version_callback, is_eager=True,
    help="print the program version and exit")


class Switch(str, Enum):
    off = "off"
    on = "on"


@app.callback(no_args_is_help=True)
def callback(version: bool = VersionOption):
    """
    a controller for the display and fan of the Raspberry Pi Power Over Ethernet HAT (Type B),
    compatible with Raspberry Pi 3B+/4B.

    Use the `run` command to show resource information on the display and control the fan based
    on the temperature of your Raspi. Also, there are other commands to control fan and display
    directly.
    """


@app.command()
def run(
    fan_on_temp: float = 53,
    fan_off_temp: float = 48,
    frame_time: float = 2.0
):
    """
    start the display and fan controller
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
    logger.info("Starting Raspi PoE HAT Monitor")
    ctrl = Controller(fan_on_temp=fan_on_temp, fan_off_temp=fan_off_temp, frame_time=frame_time)
    ctrl.main_loop()


@app.command()
def fan(switch: Switch):
    """
    control the fan of the PoE HAT; no speed control, just on and off
    """
    poe_hat = PoeHat()
    if switch == Switch.off:
        poe_hat.fan_off()
    elif switch == Switch.on:
        poe_hat.fan_on()
    else:
        raise ValueError(f"unexpected value {switch=}")


@app.command()
def clear():
    """
    clear the display and turn it off
    """
    PoeHat().display_clear()


@app.command()
def text(content: str, mode: str):
    """
    show some text of your own choosing on the display
    """
    # text with different modes: center, marquee, ...?
    print("not yet implemented")


if __name__ == "__main__":
    app()
