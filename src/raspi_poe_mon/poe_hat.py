from contextlib import contextmanager

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL.ImageDraw import ImageDraw


class PoeHat:

    def __init__(self) -> None:
        self.i2c_fan = i2c(port=1, address=0x20)
        self.i2c_display = i2c(port=1, address=0x3C)
        self.display = ssd1306(serial_interface=self.i2c_display, width=128, height=32)

    def fan_on(self):
        self.i2c_fan.command(0xFE)

    def fan_off(self):
        self.i2c_fan.command(0x01)

    @contextmanager
    def draw(self) -> ImageDraw:
        with canvas(self.display) as draw:
            yield draw
