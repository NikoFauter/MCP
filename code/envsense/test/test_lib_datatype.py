from envsense.lib import datatypes
import pytest


@pytest.mark.parametrize("binary,expected", [
    (0b11111111, -1),
    (0b00000000, 0),
    (0b10000000, -128),
    (0b11011110, -34),
    (0b01011100, 92)
])
def test_get_int_from_byte(binary, expected):
    assert datatypes.get_int_from_byte(binary) == expected


@pytest.mark.parametrize("binary,expected", [
    (0b110001000, 0b01010000),
    (0b100001111, 0b00001001)
])
def test_exception_get_int_from_byte(binary, expected):
    with pytest.raises(ValueError):
        assert datatypes.get_int_from_byte(binary) == expected


@pytest.mark.parametrize("binary,expected", [
    (0b11111111, 255),
    (0b00000000, 0),
    (0b10000000, 128),
    (0b11011110, 222),
    (0b01011100, 92)
])
def test_get_int_from_ubyte(binary, expected):
    assert datatypes.get_int_from_ubyte(binary) == expected


@pytest.mark.parametrize("binary,expected", [
    (0b101000000, 0b01010000),
    (0b100001111, 0b00001001)
])
def test_exception_get_int_from_ubyte(binary, expected):
    with pytest.raises(ValueError):
        assert datatypes.get_int_from_ubyte(binary) == expected


@pytest.mark.parametrize("binary,expected", [
    (0b1111111111111111, -1),
    (0b00000000, 0),
    (0b000000000000, 0),
    (0b1000000000000000, -32768),
    (0b1000000010000000, -32640),
    (0b0000000011011110, 222),
])
def test_get_int_from_short(binary, expected):
    assert datatypes.get_int_from_short(binary) == expected


@pytest.mark.parametrize("binary,expected", [
    (0b11001011110001000, 0b01010000),
    (0b11111110100001111, 0b00001001)
])
def test_exception_get_int_from_short(binary, expected):
    with pytest.raises(ValueError):
        assert datatypes.get_int_from_short(binary) == expected


@pytest.mark.parametrize("binary,expected", [
    (0b11111111, 255),
    (0b1111111111111111, 65535),
    (0b00000000, 0),
    (0b0000000010000000, 128),
    (0b11011110, 222),
])
def test_get_int_from_ushort(binary, expected):
    assert datatypes.get_int_from_ushort(binary) == expected


@pytest.mark.parametrize("binary,expected", [
    (0b11001011110001000, 0b01010000),
    (0b11111110100001111, 0b00001001)
])
def test_exception_get_int_from_ushort(binary, expected):
    with pytest.raises(ValueError):
        assert datatypes.get_int_from_ushort(binary) == expected
