# Raspi PoE HAT Monitor

A controller for the display and fan of the Raspberry Pi Power Over Ethernet HAT (Type B), compatible with Raspberry Pi 3B+/4B.

## Getting Started

To set up your local development environment, please run:

    poetry install

Behind the scenes, this creates a virtual environment and installs `raspi_poe_mon` along with its dependencies into a new virtualenv. Whenever you run `poetry run <command>`, that `<command>` is actually run inside the virtualenv managed by poetry.

If you run this command on Raspberry Pi OS, it may get stuck due to issues with gnome-keyring. If this is the case, please `export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` and try again.

You should now be able to access the CLI with `poetry run python -m raspi_poe_mon`.

### Testing

We use `pytest` as test framework. To execute the tests, please run

    pytest tests

To run the tests with coverage information, please use

    pytest tests --cov=src --cov-report=html --cov-report=term

and have a look at the `htmlcov` folder, after the tests are done.

### Distribution Package

To build a distribution package (wheel), please use

    poetry build

this will create a wheel package in the dist folder.

### Contributions

Before contributing, please set up the pre-commit hooks to reduce errors and ensure consistency

    pip install -U pre-commit
    pre-commit install

If you run into any issues, you can remove the hooks again with `pre-commit uninstall`.

## Contact

Sebastian Straub (sstraub@posteo.de)

## License

© Sebastian Straub
