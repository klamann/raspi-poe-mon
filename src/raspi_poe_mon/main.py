import logging
from enum import Enum
from typing import Annotated, Optional

import typer

from raspi_poe_mon import __title__, __version__
from raspi_poe_mon.ctrl import Controller
from raspi_poe_mon.poe_hat import PoeHat

logger = logging.getLogger('raspi_poe_mon')
app = typer.Typer(name='raspi-poe-mon')


def version_callback(value: bool):
    if value:
        print(f"{__title__} {__version__}")
        raise typer.Exit()


class Switch(str, Enum):
    off = "off"
    on = "on"


@app.callback(
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]}
)
def callback(
    version: Annotated[
        Optional[bool], typer.Option(
            '--version',
            '-v',
            callback=version_callback,
            is_eager=True,
            help="print the program version and exit"
        )
    ] = None
):
    """
    a controller for the display and fan of the Raspberry Pi Power Over Ethernet HAT (Type B),
    compatible with Raspberry Pi 3B+/4B.

    Use the `run` command to show resource information on the display and control the fan based
    on the temperature of your Raspi. Also, there are other commands to control fan and display
    directly. Check the help for each sub-command to learn more, e.g. `raspi-poe-mon run --help`
    """


@app.command()
def run(
    fan_on_temp: Annotated[
        float,
        typer.Option(help="turn on the fan when CPU temperature rises above this value (in °C)")
    ] = 60,
    fan_off_temp: Annotated[
        float,
        typer.Option(help="turn off the fan when CPU temperature drops below this value (in °C)")
    ] = 50,
    frame_time: Annotated[
        float,
        typer.Option(help="update the display every n seconds")
    ] = 2.0,
    verbose: Annotated[
        bool,
        typer.Option(help="log detailed status information")
    ] = False,
    dry: Annotated[
        bool,
        typer.Option(help="dry run - simulate commands without accessing the PoE HAT")
    ] = False,
):
    """
    activate the display and fan controller.

    the display will show system information (IP address, CPU, RAM, disk, temperature).
    the fan will turn on when CPU temperature gets above a certain threshold.
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s [%(levelname)s]: %(message)s")
    logger.info(f"Starting Raspi PoE HAT Monitor, version {__version__}")
    ctrl = Controller(
        fan_on_temp=fan_on_temp,
        fan_off_temp=fan_off_temp,
        frame_time=frame_time,
        dry_run=dry
    )
    ctrl.main_loop()


@app.command()
def fan(
    switch: Annotated[
        Switch, typer.Argument(case_sensitive=False, help="turn the fan OFF or ON")
    ]
):
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
    show some text of your own choosing on the display (not available yet)
    """
    # text with different modes: center, marquee, ...?
    print("not yet implemented")


if __name__ == "__main__":
    app()
