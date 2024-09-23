import logging
import os

from luma.emulator.device import capture

from raspi_poe_mon.monitor import SystemMonitor
from raspi_poe_mon.poe_hat import PoeHat
from tests import root_dir

logger = logging.getLogger('raspi_poe_mon')


def test_draw_emulated_image():
    data_dir = root_dir / 'data'
    data_dir.mkdir(exist_ok=True)
    emulator = capture(
        width=128,
        height=32,
        mode="1",
        scale=1,
        file_template=str(data_dir) + "/luma_{0:06}.png"
    )
    poe_hat = PoeHat()
    # patch in the emulator and don't connect via i2c
    poe_hat.display = emulator
    poe_hat.display_connect = lambda force=False: None
    # draw a frame using the emulator
    renderer = SystemMonitor(poe_hat)
    renderer.draw_frame()
    logger.debug(f"files in {data_dir}: {os.listdir(data_dir)}")
    screenshot = data_dir / 'luma_000001.png'
    assert screenshot.exists()
    assert screenshot.stat().st_size > 0
