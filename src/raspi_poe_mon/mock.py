from luma.core import render
from luma.core.interface import serial
from luma.oled import device


def monkeypatch():
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


class MockFan:
    """replacement for i2c fan in dry run mode"""

    def __init__(self, *args, **kwargs):
        pass

    def command(self, *args, **kwargs):
        return


class MockCanvas(render.canvas):
    """behaves like luma's canvas, but does not actually send data to the display"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __exit__(self, type, value, traceback):
        del self.draw
        return
