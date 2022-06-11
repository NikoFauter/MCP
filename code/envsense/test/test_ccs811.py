import pytest

from envsense.lib import hal
from envsense.devices.ccs811 import CCS811
from envsense.test.mock_i2c import MockI2C
import envsense.test.register_maps as reg_maps


@pytest.fixture
def mock_base_class():
    CCS811.__bases__ = (MockI2C,)


def test_get_hardware_id(mock_base_class):
    ccs811 = CCS811(1, hal.ADDR_CCS811)
    assert ccs811.get_hardware_id() == hal.HARDWARE_ID_CCS811


def test_check_device(mock_base_class):
    ccs811 = CCS811(1, hal.ADDR_CCS811)
    assert ccs811.check_device()


def test_get_status(mock_base_class):
    ccs811 = CCS811(1, hal.ADDR_CCS811)
    assert ccs811.get_status() == 0x42


def test_app_start(mock_base_class):
    ccs811 = CCS811(1, hal.ADDR_CCS811)
    pass  # TODO currently not testable


def test_get_error_id(mock_base_class):
    ccs811 = CCS811(1, hal.ADDR_CCS811)
    assert ccs811.get_error_id() == 0x43


@pytest.mark.parametrize("mode", [0, 1, 2, 3, 4])
def test_set_mode(mock_base_class, mode):
    ccs811 = CCS811(1, hal.ADDR_CCS811)
    ccs811._set_mode(mode)
    assert (reg_maps.ccs811[hal.REG_CCS811_MEAS_MODE] >> 4) & 0b111 == mode


@pytest.mark.parametrize("mode", [-1, 5, 6])
def test_set_mode_assert_error(mock_base_class, mode):
    ccs811 = CCS811(1, hal.ADDR_CCS811)
    with pytest.raises(AssertionError):
        ccs811._set_mode(mode)


def test_read_values(mock_base_class):
    ccs811 = CCS811(1, hal.ADDR_CCS811)
    assert ccs811.read_values() == (467, 11)


def test_get_tvoc(mock_base_class):
    ccs811 = CCS811(1, hal.ADDR_CCS811)
    assert ccs811.get_tvoc() == 11


def test_raw_data(mock_base_class):
    ccs811 = CCS811(1, hal.ADDR_CCS811)
    assert ccs811.raw_data() == (7, 409)
