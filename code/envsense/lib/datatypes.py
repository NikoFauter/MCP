import ctypes

# These methods converts different data types to int.
# For implementation you might want to consult the documentation of ctypes.
# Whenever input data does not match the expected type (i.e. exceeds its
# maximum value), a ValueError should be raised.


def get_int_from_byte(binary):

    if binary > 255:
        raise ValueError

    if binary & 1 << 7 != 0:
        binary -= 1
        inverted_binary = (~binary) & 0xFF

        result = -int(inverted_binary)
    else:
        result = int(binary)
    return result
    pass


def get_int_from_ubyte(binary):
    if binary > 256:
        raise ValueError
    return int(binary)
    pass


def get_int_from_short(binary):
    if binary >= 1 << 16:
        raise ValueError

    if binary & 1 << 15 != 0:
        binary -= 1
        inverted_binary = (~binary) & 2**16-1

        result = -int(inverted_binary)
    else:
        result = int(binary)
    return result


def get_int_from_ushort(binary):
    if binary >= 1 << 16:
        raise ValueError
    return int(binary)
    pass
