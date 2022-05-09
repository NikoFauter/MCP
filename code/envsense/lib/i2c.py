from smbus2 import SMBus


class I2C(object):
    def __init__(self, bus_id, address):
        self.busId = bus_id
        self.address = address
        self.bus = SMBus(self.busId)

    def get_registers(self, register, length=1):
        if length == 1:
            return \
                self.bus.read_i2c_block_data(self.address, register, length)[
                    0]
        else:
            return self.bus.read_i2c_block_data(self.address, register, length)

    def print_register(self, register, length=1):
        print("{0:b}".format(self.get_registers(register, length)))

    def set_register(self, register, value):
        if isinstance(value, list):
            return self.bus.write_i2c_block_data(self.address, register, value)
        else:
            return self.bus.write_byte_data(self.address, register, value)

    def get_bus(self):
        return self.bus
