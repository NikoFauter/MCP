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

    # Load default serif font
    font = ImageFont.load_default()
    # Small border around the display
    draw.rectangle((0, 0, oled.width - 1, oled.height - 1), outline=1, fill=0)
    # Hello World :)
    draw.text((74, 15), 'Hello', font=font, fill=1)
    draw.text((90, 35), 'HWP!', font=font, fill=1)
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
