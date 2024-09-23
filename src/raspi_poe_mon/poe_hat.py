from contextlib import contextmanager
from typing import Optional

from luma.core import render
from luma.core.interface import serial
from luma.oled import device
from PIL.ImageDraw import ImageDraw

from raspi_poe_mon import mock


class PoeHat:

    def __init__(self, dry_run=False, brightness=100) -> None:
        self.dry_run = dry_run
        self.brightness = brightness
        self.i2c_fan: Optional[serial.i2c] = None
        self.i2c_display: Optional[serial.i2c] = None
        self.display: Optional[device.ssd1306] = None
        self.fan_state = False
        if self.dry_run:
            mock.monkeypatch()

    def fan_connect(self, force=False):
        if force or self.i2c_fan is None:
            self.i2c_fan = serial.i2c(port=1, address=0x20)

    def display_connect(self, force=False):
        if force or self.i2c_display is None:
            self.i2c_display = serial.i2c(port=1, address=0x3C)
        if force or self.display is None:
            self.display = device.ssd1306(serial_interface=self.i2c_display, width=128, height=32)
            self.display.contrast(int(255 * self.brightness / 100))

    def display_white(self):
        self.display_connect()
        with self.draw() as draw:
            draw.rectangle([(0, 0), (128, 32)], fill=1)

    def display_clear(self):
        self.display_connect()
        self.display.cleanup()

    def fan_on(self):
        self.fan_connect()
        self.i2c_fan.command(0xFE)
        self.fan_state = True

    def fan_off(self):
        self.fan_connect()
        self.i2c_fan.command(0x01)
        self.fan_state = False

    def is_fan_on(self) -> bool:
        return self.fan_state

    @contextmanager
    def draw(self) -> ImageDraw:
        self.display_connect()
        with render.canvas(self.display) as draw:
            yield draw

    def cleanup(self):
        self.fan_off()
        self.display_clear()
