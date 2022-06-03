import ctypes
from curses.ascii import ctrl
import math
from multiprocessing import sharedctypes
from multiprocessing.sharedctypes import Value
from ctypes import c_int64
import os
from this import d

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
        invalid = temp_oversample < 0 | hum_oversample < 0
        invalid = invalid | press_oversample < 0
        invalid = invalid | temp_oversample > 16
        invalid = invalid | hum_oversample > 16 | press_oversample > 16
        if invalid:
            raise ValueError
        t_reg = 0
        if temp_oversample != 0:
            t_reg = math.log2(temp_oversample)+1
        if(round(t_reg) != t_reg):
            raise ValueError
        h_reg = 0
        if hum_oversample != 0:
            h_reg = math.log2(hum_oversample)+1
        if(round(h_reg) != h_reg):
            raise ValueError
        p_reg = 0
        if press_oversample != 0:
            p_reg = math.log2(press_oversample)+1
        if(round(t_reg) != t_reg):
            raise ValueError

        ctrl_meas = self.get_registers(hal.REG_BME280_CTRL_MEAS)
        maskTempPress = hal.MASK_BME280_CTRL_MEAS_OSRS_T
        maskTempPress = maskTempPress | hal.MASK_BME280_CTRL_MEAS_OSRS_P
        t_reg_offset = int(t_reg) << hal.OFFSET_BME280_CTRL_MEAS_OSRS_T
        p_reg_offset = int(p_reg) << hal.OFFSET_BME280_CTRL_MEAS_OSRS_P
        valTempPress = t_reg_offset | p_reg_offset
        ctrl_meas = bit.set_mask(ctrl_meas, maskTempPress, valTempPress)
        self.set_register(hal.REG_BME280_CTRL_MEAS, ctrl_meas)
        ctrl_hum = self.get_registers(hal.REG_BME280_CTRL_HUM, 1)
        ctrl_hum = bit.set_mask(ctrl_hum, 7, int(h_reg))
        self.set_register(hal.REG_BME280_CTRL_HUM, ctrl_hum)

        pass

    def set_normal_operation_mode(self):
        mask = hal.MASK_BME280_CTRL_MEAS_MODE
        binary = self.get_registers(hal.REG_BME280_CTRL_MEAS)
        Value = bit.set_mask(binary, mask, 0b11)
        self.set_register(hal.REG_BME280_CTRL_MEAS, Value)
        pass

    def _get_temperature_compensation(self):
        dig_T1 = self.get_registers(hal.REG_BME280_DIG_T1, 2)
        dig_T1 = dig_T1[1] << 8 | dig_T1[0]
        dig_T1 = datatypes.get_int_from_ushort(dig_T1)
        dig_T2 = self.get_registers(hal.REG_BME280_DIG_T2, 2)
        dig_T2 = dig_T2[1] << 8 | dig_T2[0]
        dig_T2 = datatypes.get_int_from_short(dig_T2)
        dig_T3 = self.get_registers(hal.REG_BME280_DIG_T3, 2)
        dig_T3 = dig_T3[1] << 8 | dig_T3[0]
        dig_T3 = datatypes.get_int_from_short(dig_T3)
        return (dig_T1, dig_T2, dig_T3)

    def _get_pressure_compensation(self):
        dig_P = self.get_registers(hal.REG_BME280_DIG_P1, 18)
        dig_P1 = dig_P[1] << 8 | dig_P[0]
        dig_P1 = datatypes.get_int_from_ushort(dig_P1)
        result = [dig_P1]
        for dig_Pi in range(1, 9):
            temp = dig_P[dig_Pi*2+1] << 8 | dig_P[dig_Pi*2]
            temp = datatypes.get_int_from_short(temp)
            result.append(temp)
        return result
        pass

    def _get_humidity_compensation(self):
        dig_H1 = self.get_registers(hal.REG_BME280_DIG_H1, 1)
        dig_H1 = datatypes.get_int_from_ubyte(dig_H1)
        result = [dig_H1]

        dig_HE = self.get_registers(hal.REG_BME280_DIG_H2, 7)

        dig_H2 = dig_HE[1] << 8 | dig_HE[0]
        dig_H2 = datatypes.get_int_from_short(dig_H2)
        result.append(dig_H2)

        dig_H3 = dig_HE[2]
        dig_H3 = datatypes.get_int_from_ubyte(dig_H3)
        result.append(dig_H3)

        dig_H4 = dig_HE[3] << 4 | (dig_HE[4] & 15)
        dig_H4 = datatypes.get_int_from_short(dig_H4)
        result.append(dig_H4)

        dig_H5 = dig_HE[5] << 4 | ((dig_HE[4] & ~15) >> 4)
        print("HE[5]=", bin(dig_HE[5] << 4))
        print("HE[4][7:4]=", bin((dig_HE[4] & ~15) >> 4))

        print("H5=", bin(dig_H5))
        dig_H5 = datatypes.get_int_from_short(dig_H5)
        result.append(dig_H5)

        print("H5=", bin(2304))
        dig_H6 = datatypes.get_int_from_byte(dig_HE[6])
        result.append(dig_H6)

        return result

    def compensate_temperature(self, dig_t1, dig_t2, dig_t3, adc_t):

        var1 = ((adc_t)/16384.0 - (dig_t1)/1024.0) * (dig_t2)
        var2 = ((adc_t)/131072.0 - (dig_t1)/8192.0)
        var2 *= ((adc_t)/131072.0 - (dig_t1)/8192.0) * (dig_t3)
        T = (var1 + var2)/5120.0
        t_fine = (var1 + var2)
        return T
        pass

    pass

    def compensate_pressure(self, dig_p1, dig_p2, dig_p3, dig_p4, dig_p5,
                            dig_p6, dig_p7, dig_p8, dig_p9, adc_p):

        var1 = self.t_fine/2.0 - 64000.0
        var2 = var1 * var1 * dig_p6 / 32768.0
        var2 = var2 + var1 * dig_p5 * 2.0
        var2 = (var2/4.0)+((dig_p4) * 65536.0)
        var1 = ((dig_p3) * var1 * var1 / 524288.0 + (dig_p2) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0)*(dig_p1)
        if (var1 == 0.0):
            return 0  # avoid exception caused by division by zero
        p = 1048576.0 - adc_p
        p = (p - (var2 / 4096.0)) * 6250.0 / var1
        var1 = (dig_p9) * p * p / 2147483648.0
        var2 = p * (dig_p8) / 32768.0
        p = p + (var1 + var2 + (dig_p7)) / 16.0
        return p
        pass

    pass

    def compensate_humidity(self, dig_h1, dig_h2, dig_h3, dig_h4, dig_h5,
                            dig_h6, adc_h):

        var_h1 = (self.t_fine) - 76800.0
        var_h2 = (adc_h - ((dig_h4) * 64.0 + (dig_h5) / 16384.0 * var_h1))
        var_h5 = (1.0 + (dig_h3) / (67108864.0 * var_h1))
        var_h3 = (1.0 + (dig_h6) / 67108864.0 * var_h1 * var_h5)
        var_h4 = ((dig_h2) / 65536.0 * var_h3)
        var_h = var_h2 * var_h4

        var_h = var_h * (1.0 - (dig_h1) * var_h / 524288.0)
        if (var_h > 100.0):
            var_h = 100.0
        else:
            if (var_h < 0.0):
                var_h = 0.0
        return var_h

    def get_temperature(self):
        Temp_array = self.get_registers(hal.REG_BME280_TEMP, 3)
        Temp_MSB = Temp_array[0]
        Temp_LSB = Temp_array[1]
        Temp_xLSB = Temp_array[2] >> 4
        T = int(Temp_MSB << 12 | Temp_LSB << 4 | Temp_xLSB)
        (dig_t1, dig_t2, dig_t3) = self._get_temperature_compensation()
        return self.compensate_temperature(dig_t1, dig_t2, dig_t3, T)
        pass

    def get_pressure(self):
        Press_array = self.get_registers(hal.REG_BME280_PRESS, 3)
        Press_MSB = Press_array[0]
        Press_LSB = Press_array[1]
        Press_xLSB = Press_array[2] >> 4
        P = int(Press_MSB << 12 | Press_LSB << 4 | Press_xLSB)
        (dig_p1, dig_p2, dig_p3, dig_p4, dig_p5, dig_p6, dig_p7, dig_p8, dig_p9) = self._get_pressure_compensation()
        return self.compensate_pressure(dig_p1, dig_p2, dig_p3, dig_p4, dig_p5, dig_p6, dig_p7, dig_p8, dig_p9,  P)
        pass

    def get_humidity(self):
        Hum_array = self.get_registers(hal.REG_BME280_HUM, 2)
        Hum_MSB = Hum_array[0]
        Hum_LSB = Hum_array[1]
        H = int(Hum_MSB << 8 | Hum_LSB)
        (dig_h1, dig_h2, dig_h3, dig_h4, dig_h5, dig_h6) = self._get_humidity_compensation()
        return self.compensate_humidity(dig_h1, dig_h2, dig_h3, dig_h4, dig_h5, dig_h6, H)
        pass
