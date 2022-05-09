import pytest

from envsense.lib import hal
from envsense.devices.bme280 import BME280
from envsense.test.mock_i2c import MockI2C


@pytest.fixture
def mock_base_class():
    BME280.__bases__ = (MockI2C,)


@pytest.mark.parametrize(
    "dig_t1, dig_t2, dig_t3, adc_t, expected_float, expected_int", [
        (15, 79, 107, 12, -0.0002146565364455455, 0),
        (28376, 26959, 50, 530752, 24.66448075110093, 24.66),
    ])
def test_compensate_temperature(mock_base_class, dig_t1, dig_t2, dig_t3, adc_t,
                                expected_float, expected_int):
    bme280 = BME280(1, hal.ADDR_BME280)
    val = bme280.compensate_temperature(dig_t1, dig_t2, dig_t3, adc_t)
    assert val == pytest.approx(expected_float) or val == expected_int


@pytest.mark.parametrize("dig_p1, dig_p2, dig_p3, dig_p4, dig_p5, dig_p6, "
                         "dig_p7, dig_p8, dig_p9, adc_p, expected_float, "
                         "expected_int", [
                             (36737, -10548, 3024, 8443, -83, -7, 9900,
                              -10230, 4285, 352368, 91512.31800532545,
                              91512.31640625),
                             (37643, -10514, 3024, 6805, -105, -7, 9900,
                              -10230, 4285, 367504, 91055.50201802237,
                              91055.5)
                         ])
def test_compensate_pressure(mock_base_class, dig_p1, dig_p2, dig_p3, dig_p4,
                             dig_p5, dig_p6, dig_p7, dig_p8, dig_p9, adc_p,
                             expected_float, expected_int):
    bme280 = BME280(1, hal.ADDR_BME280)

    # Internal state used for compensation.
    # Assume no previous temperature measurement
    bme280.t_fine = 0
    val = bme280.compensate_pressure(
        dig_p1, dig_p2, dig_p3, dig_p4, dig_p5, dig_p6, dig_p7, dig_p8, dig_p9,
        adc_p)
    assert val == pytest.approx(expected_float) or val == expected_int


@pytest.mark.parametrize("dig_h1, dig_h2, dig_h3, dig_h4, dig_h5, dig_h6, "
                         "adc_h, expected_float, expected_int", [
                             (24, -28672, 200, -384, -2304, -52, 100, 0, 0),
                             (
                                 75, 366, 0, 310, 54, 30, 26078,
                                 34.83120937498718, 34.8359375)
                         ])
def test_compensate_humidity(mock_base_class, dig_h1, dig_h2, dig_h3, dig_h4,
                             dig_h5, dig_h6, adc_h, expected_float,
                             expected_int):
    bme280 = BME280(1, hal.ADDR_BME280)

    # Internal state used for compensation.
    # Assume no previous temperature measurement
    bme280.t_fine = 0
    val = bme280.compensate_humidity(
        dig_h1, dig_h2, dig_h3, dig_h4, dig_h5, dig_h6, adc_h)
    assert val == pytest.approx(expected_float) or val == expected_int


def test_set_normal_operation_mode(mock_base_class):
    bme280 = BME280(1, hal.ADDR_BME280)
    bme280.set_normal_operation_mode()
    assert bme280.get_registers(hal.REG_BME280_CTRL_MEAS) == 0b00001011


def test_get_temperature_compensation(mock_base_class):
    bme280 = BME280(1, hal.ADDR_BME280)
    (digT1, digT2, digT3) = bme280._get_temperature_compensation()
    assert (digT1, digT2, digT3) == (32792, -28672, -31737)


def test_get_pressure_compensation(mock_base_class):
    bme280 = BME280(1, hal.ADDR_BME280)
    (dig_P1, dig_P2, dig_P3, dig_P4, dig_p5, dig_p6, dig_p7,
     dig_p8, dig_p9,) = bme280._get_pressure_compensation()
    print(bme280._get_pressure_compensation())
    assert (dig_P1, dig_P2, dig_P3, dig_P4, dig_p5, dig_p6,
            dig_p7, dig_p8, dig_p9,) == (
           32792, -28672, -31737, -32744, -28672, -31737, -32744, -28672,
           -31737)


def test_get_humidity_compensation(mock_base_class):
    bme280 = BME280(1, hal.ADDR_BME280)
    (dig_P1, dig_P2, dig_P3, dig_P4, dig_p5,
     dig_p6) = bme280._get_humidity_compensation()
    print(bme280._get_humidity_compensation())
    assert (dig_P1, dig_P2, dig_P3, dig_P4, dig_p5, dig_p6) == (
        24, -28672, 7, 384, 2304, -52)


def test_get_temperature(mock_base_class):
    bme280 = BME280(1, hal.ADDR_BME280)
    temperature = bme280.get_temperature()
    assert temperature == pytest.approx(4.956382428682218) \
           or temperature == 4.96


def test_get_pressure(mock_base_class):
    bme280 = BME280(1, hal.ADDR_BME280)
    pressure = bme280.get_pressure()
    assert pressure == pytest.approx(143356.32443242334) \
           or pressure == 143356.328125


def test_get_humidity(mock_base_class):
    bme280 = BME280(1, hal.ADDR_BME280)
    humidity = bme280.get_humidity()
    assert humidity == pytest.approx(0)


@pytest.mark.parametrize("oversampling, register",
                         [(0, 0b000),
                          (1, 0b001),
                          (2, 0b010),
                          (4, 0b011),
                          (8, 0b100),
                          (16, 0b101)])
def test_calculate_oversampling_register_val(mock_base_class,
                                             oversampling, register):
    assert BME280._calculate_oversampling_register_val(oversampling) \
           == register


@pytest.mark.parametrize("oversampling", [-1, 3, 5, 32])
def test_calculate_oversampling_register_val_assert_error(mock_base_class,
                                                          oversampling):
    with pytest.raises(AssertionError):
        BME280._calculate_oversampling_register_val(oversampling)


@pytest.mark.parametrize("temp, hum, press, t_reg, h_reg, p_reg",
                         [(0, 0, 0, 0b000, 0b000, 0b000),
                          (4, 4, 4, 0b011, 0b011, 0b011),
                          (16, 16, 16, 0b101, 0b101, 0b101),
                          (2, 4, 8, 0b010, 0b011, 0b100),
                          (16, 2, 16, 0b101, 0b010, 0b101)])
def test_set_oversampling_mode(mock_base_class, temp, hum, press,
                               t_reg, h_reg, p_reg):
    # Humidity oversampling: osrs_h[2:0] in ctrl_hum (2 .. 0)
    # Temperature oversampling: osrs_t[2:0] in ctrl_meas (7 .. 5)
    # Preassure oversampling: osrs_p[2:0] in ctrl_meas (4 .. 2)

    bme280 = BME280(1, hal.ADDR_BME280)
    bme280.set_oversampling_mode(temp, hum, press)

    assert (bme280.get_registers(hal.REG_BME280_CTRL_MEAS) >> 5) & 0b111 \
        == t_reg
    assert bme280.get_registers(hal.REG_BME280_CTRL_HUM) & 0b111 == h_reg
    assert (bme280.get_registers(hal.REG_BME280_CTRL_MEAS) >> 2) & 0b111 \
        == p_reg
