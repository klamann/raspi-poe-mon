# Raspi PoE HAT Monitor

[![build](https://github.com/klamann/raspi-poe-mon/actions/workflows/build.yml/badge.svg?branch=main&event=push)](https://github.com/klamann/raspi-poe-mon/actions/workflows/build.yml)
[![PyPI](https://img.shields.io/pypi/v/raspi-poe-mon)](https://pypi.org/project/raspi-poe-mon/)
[![PyPI - License](https://img.shields.io/pypi/l/raspi-poe-mon)](https://github.com/klamann/raspi-poe-mon/blob/main/LICENSE)
![Raspi](https://img.shields.io/badge/Raspberry%20Pi-A22846?logo=Raspberry%20Pi&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)

A controller for the display and fan of the Raspberry Pi Power Over Ethernet HAT (Type B), compatible with Raspberry Pi 3B+/4B.

![](https://raw.githubusercontent.com/klamann/raspi-poe-mon/main/docs/raspi-poe-hat-2k.webp)

The PoE HAT ([Waveshare SKU 18014](https://www.waveshare.com/wiki/PoE_HAT_(B))) allows you to deliver gigabit ethernet connectivity and power supply to your Raspi using a single connection (if you have a PoE capable switch/router). While PoE works without additional drivers, there is also a fan and a 128x32 pixel monochrome display on the HAT, both of which can be controlled with this software.

Warning: The OLED display is susceptible to burn-in, pixel brightness will deteriorate over time - refer to section [Handling OLED burn-in](#handling-oled-burn-in) for more information.

## Features

* automatic fan control to reach your desired temperature target
* show status information on the display: IP address, CPU usage, CPU temperature, RAM usage, disk usage.
* manual fan control via CLI
* show custom text via CLI (wip)

## Getting Started

If you are running the latest [Raspberry Pi OS](https://www.raspberrypi.com/software/), everything should already be set up the way we need it and you can run

    pip install raspi-poe-mon --break-system-packages

The scary `--break-system-packages` flag just tells Python that you want to install this package globally rather than in a virtualenv. I don't agree with the framing here, in my opinion it's fine to install Python packages globally on your Raspi.

After installation finished, you can call

    raspi-poe-mon run

and the OLED disply should show you some info. Learn more about the available options with `raspi-poe-mon --help`. Each command has its own help section, e.g. `raspi-poe-mon run --help`.

### Install Guide

If you want to install `raspi-poe-mon` on older Raspberry Pi OS or on a different OS, this section is for you.

The OLED display and fan controls of the PoE HAT are accessed through the [I²C interface](https://de.wikipedia.org/wiki/I%C2%B2C), which may be deactivated by default on your Raspi. To activate it on Raspberry Pi OS, run

    sudo raspi-config nonint do_i2c 0

or call `raspi-config` without params and use the menu (`Interface Options` -> `I2C` -> `Yes`). You may need to reboot your Raspi to apply the change.

Next we install required packages: Python and pip are needed; the remaining packages are dependencies of the Pillow graphics library.

    sudo apt install python3 python3-pip libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 libsdl2-image-2.0-0

Now we are ready to install `raspi-poe-mon` from PyPI:

    pip install raspi-poe-mon

If you are using Python 3.11 or higher, you may be greeted by `error: externally-managed-environment`. You can install raspi-poe-mon in a virtual environment to avoid this message, but then you can only use the `raspi-poe-mon` CLI when you enable this virtualenv first. If you want to ignore this annoyance, you can just add the `--break-system-packages` flag and go on with your day.

### Troubleshooting

* the `raspi-poe-mon` command is not available after installation? Make sure that `$HOME/.local/bin` is on your `PATH`! On Raspi OS, this is already the case, but when this folder was just created, you might have to open a new terminal session first.
* if you try to install Python packages via pip on Raspberry Pi OS, you may get stuck due to [issues with gnome-keyring](https://github.com/pypa/pip/issues/7883). If this is the case, please `export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring` and try again. You may want to add this to your `.profile` if the issue persists.
* `pip install raspi-poe-mon` is still hangig or really slow? I can confirm that sometimes, downloading packages from PyPI on Raspi OS can take quite a while and I have no idea why... Try `pip install raspi-poe-mon -vvv` to get some status info and let it do it's thing for a couple of minutes.
* the `pip` command is not available, even after installing `python3-pip`? try `pip3` instead.

### Handling OLED burn-in

The light output of pixels in OLED displays generally decreases over time when used. Modern OLED panels in TVs and computer monitors can compensate for this kind of degradation, but the cheap monochrome display that comes with the PoE HAT does not. If usage patterns on displays are unevenly distributed, you can see pixels that are weaker than others, and over time ghost images may appear.

After a year, the display can look like this (all pixels were set to 100% brightness for this effect):

![](https://raw.githubusercontent.com/klamann/raspi-poe-mon/main/docs/oled-burn-in.webp)

*Can you guess my local IP address?*

With this display model, there's not much we can do to slow this process, except *not* using the display. [This video](https://youtu.be/GWOFF5tMv_A?t=670) shows the burn-in effect for monochrome OLED displays over the duration of a year.

The good news is: The OLED display usually does not break, even when lots of pixels are affected by burn-in. The bad news: We can't control the voltage for individual pixels and things like screensavers don't work for the kind of panel we're dealing with.

So what can we do?

* decrease display brightness. With the `--brightness` flag, we can set the brightness level from 0 to 100%, the default is 50%. The 100% setting is probably more than you need when indoors; try to find the optimal setting for your environment.
* only turn the display on every so often. Use the `--frame-time` and `--blank-time` parameters to do so, e.g. `--frame-time 5 --blank-time 10` will turn on the display for 5 seconds and then turn it off for 10 seconds.
* turn off the display when you don't need it with the `--no-display` flag. Of course, doing this manually would be impractical, but you can set up cron jobs in combination with the `--timeout` flag to schedule times when the display is on.

None of these options are a silver bullet and some may be too annoying for you to consider, but that's all I was able to come up with to improve the lifetime of these displays. If all else fails, you can buy a compatible OLED display and replace the one affected by burn-in. Any monochrome I2C display with 128x32 pixels should work, some soldering might be required.

## User Guide

After installation, the `raspi-poe-mon` command should be available on your terminal. Get usage instructions with

    raspi-poe-mon --help

To activate the display and fan controller, use

    raspi-poe-mon run

This will show live system information and control the fan on the PoE HAT based on chip temperature. Each command has its own help section that lists all avilable options, e.g. `raspi-poe-mon run --help`. This will tell you how to change the fan controller settings

    raspi-poe-mon run --fan-off-temp 50 --fan-on-temp 60 --brightness 80

With this setting, the fan will turn on when the CPU reaches 60°C and turn off after it has cooled down to 50°C. The display's brightness level is set to 80%.

### Start on Boot

The display and fan controller will only stay active as long as the process is running. To have it start automatically on boot and keep it running in the background, we can create a system service. On Raspi OS, create a new file `/etc/systemd/system/raspi-poe-mon.service` with this content:

```
[Unit]
Description=Raspi PoE HAT Monitor
After=network.target

[Service]
ExecStart=/home/raspi/.local/bin/raspi-poe-mon run --fan-off-temp 50 --fan-on-temp 60
User=raspi
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

You may have to change `User=` and adjust the path to the executable in `ExecStart=` (find it with `which raspi-poe-mon`). Here you can also change the fan control settings to your liking. Now you can activate the service with

    sudo systemctl daemon-reload
    sudo systemctl enable raspi-poe-mon
    sudo service raspi-poe-mon start

Enjoy!

### Command Line Options

**Usage**:

```console
$ raspi-poe-mon [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`: print the program version and exit
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `display`: turn the display of the PoE HAT on or off...
* `fan`: control the fan of the PoE HAT; no speed...
* `run`: activate the display and fan controller.
* `text`: show some text of your own choosing on the...

#### `raspi-poe-mon run`

activate the display and fan controller.

the display will show system information (IP address, CPU, RAM, disk, temperature).
the fan will turn on when CPU temperature gets above a certain threshold.

**Usage**:

```console
$ raspi-poe-mon run [OPTIONS]
```

**Options**:

* `--fan-on-temp FLOAT`: turn on the fan when CPU temperature rises above this value (in °C)  [default: 60]
* `--fan-off-temp FLOAT`: turn off the fan when CPU temperature drops below this value (in °C)  [default: 50]
* `--frame-time FLOAT`: show a new frame on the display every n seconds (excluding blank time)  [default: 2.0]
* `--blank-time FLOAT`: bank time (seconds) between frames where the display is turned off  [default: 0.0]
* `--brightness INTEGER RANGE`: brightness level of the display in percent  [default: 50; 0<=x<=100]
* `--timeout FLOAT RANGE`: terminate after n seconds; 0 means run until interrupted  [default: 0.0; x>=0]
* `--display / --no-display`: show system information on the display  [default: display]
* `--fan / --no-fan`: control fan speed based on temperature  [default: fan]
* `--verbose`: log detailed status information
* `--dry`: dry run - simulate commands without accessing the PoE HAT
* `--profiling`: log profiling information, very verbose
* `--help`: Show this message and exit.

#### `raspi-poe-mon display`

turn the display of the PoE HAT on or off (on means all white, useful to detect pixel failures)

turning the display OFF with this command should usually not be necessary, since raspi-poe-mon
will always turn off the display when it terminates. But if your display is stuck in the 'on'
state for some reason, you can explicitly turn it off with this command.

turning the display ON will not show any information, but it will light up all pixels, which
can be useful to detect pixel failures. Unfortunately, pixel burn-in is a known issue with
these cheap OLED displays.

**Usage**:

```console
$ raspi-poe-mon display [OPTIONS] SWITCH:{off|on}
```

**Arguments**:

* `SWITCH:{off|on}`: turn the display OFF or ON  [required]

**Options**:

* `--help`: Show this message and exit.

#### `raspi-poe-mon fan`

control the fan of the PoE HAT; no speed control, just on and off

**Usage**:

```console
$ raspi-poe-mon fan [OPTIONS] SWITCH:{off|on}
```

**Arguments**:

* `SWITCH:{off|on}`: turn the fan OFF or ON  [required]

**Options**:

* `--help`: Show this message and exit.

## Development

To set up your local development environment, please make sure that [poetry](https://python-poetry.org/docs/#installation) is installed and updated. Then clone this repo and install the package with

    poetry install

This will create a new virtualenv in the `.venv` folder, install all dependencies and then the `raspi-poe-mon` package. You should now be able to access the CLI with `poetry run raspi-poe-mon`.

We use `pytest` as test framework:

    poetry run pytest

To build a distribution package (wheel), please use

    poetry build

Before contributing code, please set up the pre-commit hooks to reduce errors and ensure consistency

    pre-commit install

## Tips & Tricks

* you can [increase the I2C baudrate](https://luma-oled.readthedocs.io/en/latest/hardware.html#enabling-the-i2c-interface) from the default 100KHz to 400KHz by adding `dtparam=i2c_arm=on,i2c_baudrate=400000` to `/boot/config.txt` and then rebooting. This will allow you to run animations at a higher framerate, but it is not required for the default status display.
* `raspi-poe-mon` might leak memory when running for a long time on specific combinations of OS and Python interpreter. I was unable to debug this issue, because the leak goes away when you attach a profiler (stupid heisenbug). If you are affected, please try to upgrade to a newer Python version or set up a cron job to restart `raspi-poe-mon` once per day.

## Links

* [raspi-poe-mon](https://github.com/klamann/raspi-poe-mon) (this project) on GitHub
* [RustBerry-PoE-Monitor](https://github.com/jackra1n/RustBerry-PoE-Monitor), another implementation in Rust
* [Waveshare: PoE HAT (B)](https://www.waveshare.com/wiki/PoE_HAT_(B))
* [luma.oled](https://github.com/rm-hull/luma.oled)
* [pillow (PIL) dependencies](https://pillow.readthedocs.io/en/latest/installation.html#external-libraries)
* [Increase I2C baudrate from the default of 100KHz to 400KHz](https://luma-oled.readthedocs.io/en/latest/hardware.html#enabling-the-i2c-interface)
* [Font: CG pixel 4x5](https://fontstruct.com/fontstructions/show/1404171/cg-pixel-4x5)

## License

This project is available under the terms of the [MIT License](./LICENSE).
