import logging
import pkgutil
import socket
import warnings
from io import BytesIO

import psutil
from PIL import ImageFont
from PIL.Image import Image
from PIL.ImageFont import FreeTypeFont

logger = logging.getLogger('raspi_poe_mon')


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
    try:
        return psutil.sensors_temperatures()['cpu_thermal'][0].current
    except (KeyError, AttributeError) as e:
        warnings.warn(f"failed to read CPU temperature: {e}", RuntimeWarning)
        return -1


def image_to_ascii(image: Image) -> str:
    """
    converts a monochrome image to ASCII art using unicode block elements

    :param image: a monochrome PIL image
    :return: ascii representation of the image
    """
    pixel_1d = list(image.getdata(0))
    pixel_2d = [pixel_1d[i:i + image.width] for i in range(0, len(pixel_1d), image.width)]
    symbols = {0b00: ' ', 0b01: '▄', 0b10: '▀', 0b11: '█'}
    ascii_buf = []
    for row_idx in range(0, image.height, 2):
        num_row = [(hi << 1) | lo for hi, lo in zip(pixel_2d[row_idx], pixel_2d[row_idx + 1])]
        ascii_buf.append(''.join(symbols[x] for x in num_row))
    ascii_image = '\n'.join(ascii_buf)
    return ascii_image
