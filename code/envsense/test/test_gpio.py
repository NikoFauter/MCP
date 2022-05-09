from envsense.lib.gpio import GPIOIn, GPIOOut
from envsense.test.mock_gpio import MockGPIO
import pytest


@pytest.fixture
def mock_base_class():
    GPIOIn.__bases__ = (MockGPIO,)
    GPIOOut.__bases__ = (MockGPIO,)


def test_test(mock_base_class):
    out = GPIOOut(3)

    out.set(True)

    inp = GPIOIn(3)
    assert inp.get() is True
