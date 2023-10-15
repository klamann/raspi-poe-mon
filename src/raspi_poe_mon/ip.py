import psutil
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import FreeTypeFont

from raspi_poe_mon import util
from raspi_poe_mon.poe_hat import PoeHat


class IpDisplay:

    def __init__(self, poe_hat: PoeHat) -> None:
        self.poe_hat = poe_hat
        self.font_5px = util.load_font(size=5)
        self.font_8px = util.load_font('res/pcsenior-8px.ttf', size=8)
        self.font_10px = util.load_font(size=10)

    def draw_frame(self):
        ip = util.get_ip_address()
        temp = util.get_cpu_temp()
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        with self.poe_hat.draw() as draw:
            draw: ImageDraw

            # format all the contents we want to print
            cpu_f, cpu_len = self.format_number(cpu, draw, self.font_8px)
            temp_f, temp_len = self.format_number(temp, draw, self.font_8px)
            ram_f, ram_len = self.format_number(ram.percent, draw, self.font_8px)
            disk_f, disk_len = self.format_number(disk.percent, draw, self.font_8px)

            # top center: IP address
            ip_x = (128 - draw.textlength(ip, font=self.font_8px)) // 2
            draw.text((ip_x, 0), ip, font=self.font_8px, fill=1)

            # middle left: CPU
            draw.text((34 - cpu_len, 14), cpu_f, font=self.font_8px, fill=1)
            draw.text((35, 14), '%', font=self.font_8px, fill=1)
            draw.text((45, 15), "CPU", font=self.font_5px, fill=1)

            # bottom left: RAM
            draw.text((34 - ram_len, 25), ram_f, font=self.font_8px, fill=1)
            draw.text((35, 25), '%', font=self.font_8px, fill=1)
            draw.text((45, 26), "RAM", font=self.font_5px, fill=1)

            # middle right: Temperature
            draw.text((98 - temp_len, 14), temp_f, font=self.font_8px, fill=1)
            draw.text((99, 13), '°', font=self.font_8px, fill=1)
            draw.text((105, 14), 'C', font=self.font_8px, fill=1)

            # bottom right: Disk usage
            draw.text((98 - disk_len, 25), disk_f, font=self.font_8px, fill=1)
            draw.text((99, 25), '%', font=self.font_8px, fill=1)
            draw.text((109, 26), "DISK", font=self.font_5px, fill=1)

    @classmethod
    def format_number(cls, num: float, draw: ImageDraw, font: FreeTypeFont) -> tuple[str, int]:
        num_f = f"{num:.1f}" if num < 100 else f"{num:.0f}"
        length = draw.textlength(num_f, font=font)
        return num_f, length
