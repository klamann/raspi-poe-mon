import pkgutil
from io import BytesIO

from PIL import ImageFont
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import FreeTypeFont

from raspi_poe_mon.poe_hat import PoeHat



class IpDisplay:

    def __init__(self, poe_hat: PoeHat) -> None:
        self.poe_hat = poe_hat
        self.font_5px = load_font(size=5)
        self.font_10px = load_font(size=10)

    def draw_frame(self):
        with self.poe_hat.draw() as draw:
            draw: ImageDraw
            draw.rectangle(self.poe_hat.display.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "YOLO", fill="white", font=self.font_10px)


def load_font(path='res/cg-pixel-4x5.otf', size=5, **kwargs) -> FreeTypeFont:
    font_bin = pkgutil.get_data('raspi_poe_mon', path)
    return ImageFont.truetype(BytesIO(font_bin), size=size, **kwargs)
