from time import sleep
from envsense.lib import hal
from envsense.devices.bme280 import BME280
from envsense.devices.ccs811 import CCS811
from envsense.devices.ssd1306 import ssd1306
from PIL import ImageFont, ImageDraw, Image


def display(oled, heading, value):
    pass



def run():
    print("Hello HWP")

    # Init Display module
    oled = ssd1306()
    # Setup canvas to draw on
    draw = oled.canvas

    # Initiate devises
    bme280 = BME280(1, hal.ADDR_BME280)
    ccs811 = CCS811(1, hal.ADDR_CCS811)

    # Setup devises
    bme280.set_normal_operation_mode()
    bme280.set_oversampling_mode(1, 1, 1)
    ccs811._app_start()
    ccs811._set_mode()

    # Load default serif font
    font = ImageFont.load_default()
    # Small border around the display
    draw.rectangle((0, 0, oled.width - 1, oled.height - 1), outline=1, fill=0)
    i_var = 0
    if i_var == 1:
        # Hello World :)
        draw.text((74, 15), 'Hello', font=font, fill=1)
        draw.text((90, 35), 'HWP!', font=font, fill=1)
    else:
        # temperature
        temp = bme280.get_temperature
        draw.text((74, 15), 'Temperature: ' + temp + '°C', font=font, fill=1)
        # pressure
        pres = bme280.get_pressure
        draw.text((74, 25), 'Pressure: ' + pres + '', font=font, fill=1)
        # humidity
        hum = bme280.get_humidity
        draw.text((74, 35), 'Humidity: ' + hum + '', font=font, fill=1)
        # eco2
        eco2 = ccs811.get_eco2()
        draw.text((74, 45), 'CO2: ' + eco2 + 'ppm', font=font, fill=1)
        # tvoc
        tvoc = ccs811.get_tvoc()
        draw.text((74, 55), 'Total VOC:' + tvoc + 'ppb', font=font, fill=1)
    # RPI Logo
    logo = Image.open('envsense/lib/assets/pi_logo_neg.png')
    # Note: Image is inverted
    draw.bitmap((0, 0), logo, fill=1)
    # Display canvas
    oled.display()

    pass

    # # Clear Screen
    # oled.cls()
    # # Display Off
    # oled.onoff(0)
