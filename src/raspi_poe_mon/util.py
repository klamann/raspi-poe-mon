import logging
import pkgutil
import socket
from io import BytesIO

import psutil
from PIL import ImageFont
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
    except KeyError as e:
        logger.warning(f"failed to read CPU temperature: {e}")
        return -1
