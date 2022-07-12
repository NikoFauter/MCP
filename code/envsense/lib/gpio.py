from enum import Enum
from imp import reload
from pickle import TRUE
from typing_extensions import Self

import gpiozero
from gpiozero.pins.native import NativeFactory
from envsense.lib import bit


class Direction(Enum):
    IN = 0
    OUT = 1


class GPIO(object):
    def __init__(self, number: int, direction: Direction):
        if direction == Direction.IN:
            self.pin = gpiozero.Button(number, pin_factory=NativeFactory())
        else:
            self.pin = gpiozero.LED(number, pin_factory=NativeFactory())


class GPIOIn(GPIO):
    def __init__(self, number: int):
        super().__init__(number, Direction.IN)

    def get(self) -> bool:
        return self.pin.value


class GPIOOut(GPIO):
    def __init__(self, number: int):
        super().__init__(number, Direction.OUT)

    def set(self, state: bool):
        self.pin.value = state


class GPIOS():
    def __init__(self):
        Button0 = GPIOIn(4)
        Button1 = GPIOIn(7)
        Button2 = GPIOIn(27)
        Button3 = GPIOIn(22)
        Button4 = GPIOIn(10)
        Button5 = GPIOIn(9)
        Button6 = GPIOIn(11)
        Button7 = GPIOIn(5)

        self.buttons = [Button0, Button1, Button2, Button3,
                        Button4, Button5, Button6, Button7]

        LED0 = GPIOOut(6)
        LED1 = GPIOOut(13)
        LED2 = GPIOOut(19)
        LED3 = GPIOOut(26)
        LED4 = GPIOOut(12)
        LED5 = GPIOOut(7)
        LED6 = GPIOOut(8)
        LED7 = GPIOOut(25)
        self.LEDS = [LED0, LED1, LED2, LED3, LED4, LED5, LED6, LED7]
        self.on = 0

    def reload(self):
        for i in range(0, len(self.LEDS)):
            if(self.on & 1 << i != 0):
                self.LEDS[i].set(True)
            else:
                self.LEDS[i].set(False)
        pass

    def set_all(self):
        self.on = ~0
        reload
        pass

    def set_LEDS_Value(self, value):
        self.on = value
        self.reload()
        pass

    def toggle_LED_index(self, index):
        self.on = bit.toggle_bit(self.on, index)
        self.reload()

    def set_LED_index(self, index):
        self.on = bit.set_bit(self.on, index)
        self.reload
        pass

    def set_LED_index(self, index):
        self.on = bit.set_bit(self.on, index)
        self.reload()
        pass
