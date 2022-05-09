import envsense.test.register_maps as reg_maps


class MockBus(object):
    def write_byte(self, addr, byte):
        pass


class MockI2C(object):
    def __init__(self, bus_id, address):
        self.busId = bus_id
        self.address = address
        assert address in reg_maps.map_from_addr, \
            "Device not mocked, invalid address (%02x)" % address
        self.state = reg_maps.map_from_addr[address]
        self.bus = MockBus()

    def get_registers(self, register, length=1):
        # The CCS811 does not increment the address of a register on read
        # but considers them to be mailboxes, i.e. multiple bytes at one
        # address that need to be read consecutively.
        if isinstance(self.state[register], list):
            available = len(self.state[register])
            return self.state[register][:min(length, available)]

        # Normal mode, one register contains one byte
        if length > 1:
            r = []
            for i in range(length):
                r.append(self.state[register + i])
            return r
        else:
            return self.state[register]

    def print_register(self, register, length=1):
        r = []
        for i in range(length):
            r.append(self.state[register + i])
        print(r)

    def set_register(self, register, value):
        if isinstance(value, list):
            length = len(value)
        else:
            length = 1
        for i in range(length):
            self.state[register + i] = value

    def get_bus(self):
        return self.bus
