
from PIL.ImageDraw import ImageDraw

from raspi_poe_mon.poe_hat import PoeHat
from raspi_poe_mon import util


class IpDisplay:

    def __init__(self, poe_hat: PoeHat) -> None:
        self.poe_hat = poe_hat
        self.font_5px = util.load_font(size=5)
        self.font_10px = util.load_font(size=10)

    def draw_frame(self):
        ip = util.get_ip_address()
        temp = util.get_cpu_temp()
        with self.poe_hat.draw() as draw:
            draw: ImageDraw
            draw.text((2,2), ip, font=self.font_10px, fill=1)
            draw.text((2,16), f"{temp:.1f}'C", font=self.font_10px, fill=1)
