import os
if os.name == 'nt':
    from envsense.test.mock_i2c import MockI2C as I2C
else:
    from envsense.lib.i2c import I2C
from envsense.lib import hal
from envsense.lib import bit


class CCS811(I2C):
    def __init__(self, bus_id, address):
        super().__init__(bus_id, address)
        self._app_start()
        self._set_mode(1)

    def check_device(self):
        return self.get_hardware_id() == hal.HARDWARE_ID_CCS811

    def get_hardware_id(self):
        return self.get_registers(hal.REG_CCS811_HW_ID)

    def get_status(self):
        return self.get_registers(hal.REG_CCS811_STATUS)

    def _app_start(self):
        status = self.get_status()
        if (status & 1 << 4 != 0):
            print("Valid firmware already loaded")
            pass
        val = 0
        self.set_register(hal.REG_CCS811_APP_START, val)
        pass

    def get_error_id(self):
        return self.get_registers(hal.REG_CCS811_ERROR_ID)

    def _set_mode(self, mode):

        if not(0 <= mode <= 4):
            raise AssertionError
        meas_mode = self.get_registers(hal.REG_CCS811_MEAS_MODE)
        mask = 0b111 << 4
        value = mode << 4
        meas_mode = bit.set_mask(meas_mode, mask, value)
        self.set_register(hal.REG_CCS811_MEAS_MODE, meas_mode)
        pass

    def read_values(self):
        bytes = self.get_registers(hal.REG_CCS811_ALG_RESULT_DATA, 4)
        eco2 = bytes[0] << 8 | bytes[1]
        tvoc = bytes[2] << 8 | bytes[3]
        return (eco2, tvoc)

    def get_eco2(self):
        pass

    def get_tvoc(self):
        pass

    def raw_data(self):
        pass
