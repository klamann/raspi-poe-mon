# Raspi PoE HAT Monitor

A controller for the display and fan of the Raspberry Pi Power Over Ethernet HAT (Type B), compatible with Raspberry Pi 3B+/4B.

![](./docs/raspi-poe-hat-2k.webp)

## Features

* tbd

## Getting Started

The OLED display and fan controls of the PoE HAT are accessed through the I2C interface, which on Raspberry Pi OS is deactivated by default. To activate it, run

    sudo raspi-config

and select `Interface Options` -> `I2C` -> `Yes`. You need to reboot your Raspi to apply the change.

Next we install required packages: Python and pip are needed; the remaining packages are dependencies of the Pillow graphics library.

    sudo apt install python3 python3-pip libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5

Now we are ready to install `raspi-poe-mon` from PyPI:

    # TODO this is not yet available
    pip install raspi-poe-mon

You can now run `raspi-poe-mon` on your terminal to activate the display. Call `raspi-poe-mon --help` to get usage instructions.

## User Guide

tbd

## Development

To set up your local development environment, please make sure that [poetry](https://python-poetry.org/) is installed and updated

    pip install --upgrade poetry

Then install the package with

    poetry install

This will create a new virtualenv in the `.venv` folder, install all dependencies and then the `raspi-poe-mon` package. You should now be able to access the CLI with `poetry run python -m raspi_poe_mon`.

We use `pytest` as test framework:

    poetry run pytest

To build a distribution package (wheel), please use

    poetry build

Before contributing code, please set up the pre-commit hooks to reduce errors and ensure consistency

    pre-commit install

## Tips & Tricks

* You can [increase the I2C baudrate](https://luma-oled.readthedocs.io/en/latest/hardware.html#enabling-the-i2c-interface) from the default 100KHz to 400KHz by adding `dtparam=i2c_arm=on,i2c_baudrate=400000` to `/boot/config.txt` and then rebooting. This will allow you to run animations at a higher framerate.
* If you try to install Python packages via pip on Raspberry Pi OS, you may get stuck due to [issues with gnome-keyring](https://github.com/pypa/pip/issues/7883). If this is the case, please `export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` and try again. You may want to add this to your `.profile` if the issue persists.

## Links

* [Waveshare: PoE HAT (B)](https://www.waveshare.com/wiki/PoE_HAT_(B))
* [luma.oled](https://github.com/rm-hull/luma.oled)
* [pillow (PIL) dependencies](https://pillow.readthedocs.io/en/latest/installation.html#external-libraries)
* [Increase I2C baudrate from the default of 100KHz to 400KHz](https://luma-oled.readthedocs.io/en/latest/hardware.html#enabling-the-i2c-interface)
* [Font: CG pixel 4x5](https://fontstruct.com/fontstructions/show/1404171/cg-pixel-4x5)

## License

This project is available under the terms of the [MIT License](./LICENSE).
