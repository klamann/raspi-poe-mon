# Raspi PoE HAT Monitor

A controller for the display and fan of the Raspberry Pi Power Over Ethernet HAT (Type B), compatible with Raspberry Pi 3B+/4B.

## Getting Started

To set up your local development environment, please make sure that [poetry](https://python-poetry.org/) is installed and updated

    pip install --upgrade poetry

Then install the package with

    poetry install

This will create a new virtualenv in the `.venv` folder, install all dependencies and then the raspi-poe-mon package. You should now be able to access the CLI with `poetry run python -m raspi_poe_mon`.

If you try to install Python packages via pip on Raspberry Pi OS, you may get stuck due to [issues with gnome-keyring](https://github.com/pypa/pip/issues/7883). If this is the case, please `export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` and try again.

We use `pytest` as test framework. To execute the tests, please run

    pytest

To build a distribution package (wheel), please use

    poetry build

Before contributing code, please set up the pre-commit hooks to reduce errors and ensure consistency

    pre-commit install

## Contact

Sebastian Straub (sstraub [at] posteo.de)

## License

This project is available under the terms of the [MIT License](./LICENSE).
