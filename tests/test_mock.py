from raspi_poe_mon.mock import HardwarePatcher


def test_hardware_patcher():
    assert HardwarePatcher.is_real() is True
    HardwarePatcher.patch()
    assert HardwarePatcher.is_real() is False
    HardwarePatcher.restore()
    assert HardwarePatcher.is_real() is True
