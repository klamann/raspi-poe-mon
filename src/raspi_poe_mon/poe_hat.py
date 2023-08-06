from contextlib import contextmanager
from typing import Optional

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL.ImageDraw import ImageDraw


class PoeHat:

    def __init__(self) -> None:
        self.i2c_fan = i2c(port=1, address=0x20)
        self.i2c_display = i2c(port=1, address=0x3C)
        self.display: Optional[ssd1306] = None
        self.fan_state = False

    def display_connect(self):
        if self.display is None:
            self.display = ssd1306(serial_interface=self.i2c_display, width=128, height=32)

    def fan_on(self):
        self.i2c_fan.command(0xFE)
        self.fan_state = True

    def fan_off(self):
        self.i2c_fan.command(0x01)
        self.fan_state = False

    def is_fan_on(self) -> bool:
        return self.fan_state

    @contextmanager
    def draw(self) -> ImageDraw:
        self.display_connect()
        with canvas(self.display) as draw:
            yield draw

    def cleanup(self):
        self.fan_off()
        self.display.cleanup()
