from envsense.lib import bit
import pytest


@pytest.mark.parametrize("binary,offset,expected", [
    (0b00001111, 7, 0b10001111),
    (0b11111111, 3, 0b11111111),
    (0b00000000, 4, 0b00010000),
    (0b00001111, 8, 0b100001111),
    (0b00001111, 0, 0b00001111),
])
def test_set_bit(binary, offset, expected):
    assert bit.set_bit(binary, offset) == expected


@pytest.mark.parametrize("binary,offset,expected", [
    (0b00001111, 7, 0b00001111),
    (0b11111111, 3, 0b11110111),
    (0b00000000, 4, 0b00000000),
    (0b00001111, 8, 0b000001111),
    (0b00001111, 0, 0b00001110),
])
def test_clear_bit(binary, offset, expected):
    assert bit.clear_bit(binary, offset) == expected


@pytest.mark.parametrize("binary,offset,expected", [
    (0b00001111, 7, 0b10001111),
    (0b11111111, 3, 0b11110111),
    (0b00000000, 4, 0b00010000),
    (0b00001111, 8, 0b100001111),
    (0b00001111, 0, 0b00001110),
])
def test_toggle_bit(binary, offset, expected):
    assert bit.toggle_bit(binary, offset) == expected


@pytest.mark.parametrize("binary,offset,expected", [
    (0b00001111, 7, 0),
    (0b11111111, 3, 1),
    (0b00000000, 4, 0),
    (0b00001111, 8, 0),
    (0b00001111, 0, 1),
])
def test_get_bit(binary, offset, expected):
    assert bit.get_bit(binary, offset) == expected


@pytest.mark.parametrize("binary,mask,expected", [
    (0b00001111, 0b10000000, 0b00000000),
    (0b11111111, 0b00011000, 0b00011000),
    (0b01000000, 0b01010000, 0b01000000),
    (0b00001111, 0b00011110, 0b00001110),
    (0b00001111, 0b00001001, 0b00001001),
])
def test_get_mask(binary, mask, expected):
    assert bit.get_mask(binary, mask) == expected


@pytest.mark.parametrize("binary,mask,value,expected", [
    (0b00001111, 0b10000000, 0b10000000, 0b10001111),
    (0b11111111, 0b00000111, 0b00000101, 0b11111101),
    (0b01000000, 0b01010000, 0b01010000, 0b01010000),
    (0b00100000, 0b01010000, 0b01010000, 0b01110000),
    (0b00001111, 0b111100000000, 0b111100000000, 0b111100001111),
    (0b00000000, 0b00000001, 0b0, 0b00000000),
    (0b10100110, 0b00110000, 0b00, 0b10000110)
])
def test_set_mask(binary, mask, value, expected):
    assert bit.set_mask(binary, mask, value) == expected


@pytest.mark.parametrize("binary,mask,value,expected", [
    (0b01000000, 0b01010000, 0b11010000, 0b01010000),
    (0b00001111, 0b00001001, 0b00011001, 0b00001001)
])
def test_exception_set_mask(binary, mask, value, expected):
    with pytest.raises(ValueError):
        assert bit.set_mask(binary, mask, value) == expected
