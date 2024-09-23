import logging
import time

from luma.core import render
from luma.core.interface import serial
from luma.oled import device

from raspi_poe_mon.util import image_to_ascii

logger = logging.getLogger('raspi_poe_mon')


def monkeypatch():
    """monkeypatch all real hardware so the mock version is used instead. restart to undo"""
    serial.i2c = MockFan
    device.ssd1306 = MockDisplay
    render.canvas = MockCanvas


class MockDisplay:
    """replacement for ssd1306 display in dry run mode"""

    def __init__(self, *args, **kwargs):
        self.mode = "1"
        self.width = 128
        self.height = 32
        self.size = (self.width, self.height)

    def cleanup(self):
        return

    def contrast(self, *args, **kwargs):
        return


class MockFan:
    """replacement for i2c fan in dry run mode"""

    def __init__(self, *args, **kwargs):
        pass

    def command(self, *args, **kwargs):
        return


class MockCanvas(render.canvas):
    """behaves like luma's canvas, but does not actually send data to the display"""

    last_print = time.time() - 57
    print_delay = 60

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __exit__(self, type, value, traceback):
        if (
            logger.isEnabledFor(logging.DEBUG)
            and (time.time() - self.last_print) > self.print_delay
        ):
            ascii_image = image_to_ascii(self.image)
            logger.debug(f"rendered image (next log in {self.print_delay}s):\n" + ascii_image)
            MockCanvas.last_print = time.time()
        del self.draw
