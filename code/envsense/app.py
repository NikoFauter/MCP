from time import sleep
from envsense.lib import hal
from envsense.devices.bme280 import BME280
from envsense.devices.ccs811 import CCS811
from envsense.devices.ssd1306 import ssd1306
from PIL import ImageFont, ImageDraw, Image
from envsense.lib import gpio


def display(oled, bme280, ccs811, page):
    def measurement(value):
        # Take Measurements
        # temperature
        meas = {
            1: ("Temperature: ", bme280.get_temperature() + "°C"),
            # pressure
            2: ("Pressure: ", bme280.get_pressure() + " Pa"),
            # humidity
            3: ("Humidity: ", bme280.get_humidity() + " %"),
            # eco2
            4: ("CO2: ", ccs811.get_eco2() + " ppm"),
            # tvoc
            5: ("Total VOC:", ccs811.get_tvoc() + " ppb")
        }
        return meas.get(value, ("Invalid", "Measurement"))
    oled.cls
    m = measurement(page)
    draw = oled.canvas
    # Small border around the display
    draw.rectangle((0, 0, oled.width, oled.height), outline=1, fill=0)
    font1 = ImageFont.truetype('envsense/lib/assestsFreeSans.ttf', size=15)
    draw.text((2, 2), m[0],  font1, fill=1)
    font2 = ImageFont.truetype('envsense/lib/assestsFreeSans.ttf', size=18)
    size = font2.getsize(m[1])
    # Data is centered
    draw.text(
        ((oled.width-size[0])/2,
         (oled.heigth-size[1])/2),
        m[1],
        font=font2,
        fill=1)


def waiting_idly(gpios, time):
    for i in range(0, time*10):
        for k in range(1, 8):
            gpios.buttons[k].when_pressed = gpios.LEDS[k].on
            if gpios.buttons[k].is_pressed:
                return [i*0.1, k]
            sleep(0.1)
    return [time, 0]


def run():
    print("Hello HWP")

    # Init Display module
    oled = ssd1306()
    # Setup canvas to draw on
    draw = oled.canvas

    # Load default serif font
    font = ImageFont.load_default()

    # Initiate devises
    bme280 = BME280(1, hal.ADDR_BME280)
    ccs811 = CCS811(1, hal.ADDR_CCS811)

    # Setup devises
    bme280.set_normal_operation_mode()
    bme280.set_oversampling_mode(1, 1, 1)
    ccs811._app_start()
    ccs811._set_mode(2)

    # Setup GPIO
    gpios = GPIOS()

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
    sleep(1)
    oled.cls()

    test_modus = True
    test_time = 30
    if test_modus:
        draw.text((74, 15), 'Testing GPIO')
        oled.display()
        time_since_pressed = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, test_time*10):
            for i in range(0, 8):
                if gpios.buttons[i].is_pressed:
                    if time_since_pressed[i] != 0:
                        GPIOS.toggle_LED_index(i)
                        time_since_pressed[i] = 0
                else:
                    time_since_pressed[i]+0.1
            sleep(0.1)

    oled.cls()

    display_mes = True
    page = 1
    showtime = 3
    while display_mes:
        display(oled, bme280, ccs811, page)
        cmd = waiting_idly(gpios, showtime)
        if cmd == 0:
            page += 1
            if page == 7:
                page = 1
        if cmd == 1:
            page -= 1
        if cmd == 2:
            showtime -= 1
        if cmd == 3:
            showtime += 1
        if cmd == 7:
            display_mes = False

    # # Clear Screen
    oled.cls()
    # Display Off
    oled.onoff(0)
    pass

    # # Clear Screen
    # oled.cls()
    # # Display Off
    # oled.onoff(0)
