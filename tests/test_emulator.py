from luma.emulator.device import capture

from raspi_poe_mon.ip import IpDisplay
from raspi_poe_mon.poe_hat import PoeHat
from tests import root_dir


def test_foo():
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
    poe_hat.display = emulator
    ip_display = IpDisplay(poe_hat)
    ip_display.draw_frame()
    assert (data_dir / 'luma_000001.png').exists()
