import math

import os

if os.name == 'nt':
    from envsense.test.mock_i2c import MockI2C as I2C
else:
    from envsense.lib.i2c import I2C
from envsense.lib import hal
from envsense.lib import datatypes
from envsense.lib import bit


class BME280(I2C):
    chip_id = 0x60

    def __init__(self, bus_id, address):
        super().__init__(bus_id, address)
        self.t_fine = 0

    @staticmethod
    def _calculate_oversampling_register_val(val):
        assert 0 <= val <= 16 and (val == 0 or math.log(val, 2).is_integer())
        if val == 0:
            return val
        else:
            return (int(math.log(val, 2)) + 1) & 0b111

    def check_device(self):
        return self.get_chip_id() == BME280.chip_id

    def get_chip_id(self):
        return self.get_registers(hal.REG_BME280_CHIP_ID)

    def set_oversampling_mode(self, temp_oversample, hum_oversample,
                              press_oversample):
        pass

    def set_normal_operation_mode(self):
        pass

    def _get_temperature_compensation(self):
        pass

    def _get_pressure_compensation(self):
        pass

    def _get_humidity_compensation(self):
        pass

    pass

    def compensate_temperature(self, dig_t1, dig_t2, dig_t3, adc_t):
        pass

    pass

    def compensate_pressure(self, dig_p1, dig_p2, dig_p3, dig_p4, dig_p5,
                            dig_p6, dig_p7, dig_p8, dig_p9, adc_p):
        pass

    pass

    def compensate_humidity(self, dig_h1, dig_h2, dig_h3, dig_h4, dig_h5,
                            dig_h6, adc_h):
        pass

    def get_temperature(self):
        pass

    def get_pressure(self):
        pass

    def get_humidity(self):
        pass
