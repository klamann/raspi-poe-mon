import pkgutil
from io import BytesIO
import socket

from PIL import ImageFont
from PIL.ImageFont import FreeTypeFont


def load_font(path='res/cg-pixel-4x5.otf', size=5, **kwargs) -> FreeTypeFont:
    font_bin = pkgutil.get_data('raspi_poe_mon', path)
    return ImageFont.truetype(BytesIO(font_bin), size=size, **kwargs)


def get_ip_address() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # this IP is not reachable (TEST-NET-1), which is fine though, we only want our own IP
        s.connect(('192.0.2.0', 80))
        ip = s.getsockname()[0]
    return ip


def get_cpu_temp() -> float:
    with open('/sys/class/thermal/thermal_zone0/temp', 'rt') as fp:
        temp = int(fp.read()) / 1000
    return temp
