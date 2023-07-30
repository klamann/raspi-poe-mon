import logging

import typer

from raspi_poe_mon import __title__, __version__

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
    logging.basicConfig(level=logging.INFO)
    logger.info("Looks like you're all set up. Let's get going!")


if __name__ == "__main__":
    app()
