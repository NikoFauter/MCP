# Set the 'offset'-th bit in 'binary' to 1
from cgi import test


def set_bit(binary, offset):
    binary = binary | 1 << offset
    return binary
    pass


# Set the 'offset'-th bit in 'binary' to 0
def clear_bit(binary, offset):
    test = binary & 1 << offset
    if binary & 1 << offset != 0:
        binary = binary ^ (1 << offset)
    return binary
    pass


# Toggle the 'offset'-th bit in 'binary' (if it was 0, set to 1 and vice-versa)
def toggle_bit(binary, offset):
    if (binary & 1 << offset == 0):
        binary = set_bit(binary, offset)
    else:
        binary = clear_bit(binary, offset)
    return binary
    pass


# Return the 'offset'-th bit of 'binary'
def get_bit(binary, offset):
    if binary & 1 << offset == 0:
        return 0
    else:
        return 1
    pass


# Return all bits of 'binary' specified by 'mask' (marked with 1s)
def get_mask(binary, mask):
    return binary & mask
    pass


# Set all bits of 'binary' specified by 'mask' to the corresponding
# values of 'value'
def set_mask(binary, mask, value):
    i1 = 0
    if mask < value:
        raise ValueError
    while 1 << i1 <= mask:
        if(mask & 1 << i1 != 0):
            if value & 1 << i1 == 0:
                binary = clear_bit(binary, i1)
            else:
                binary = set_bit(binary, i1)

        else:
            if (mask & 1 << k1):
                raise ValueError
        k1 += 1
        i1 += 1
    return binary
    pass
