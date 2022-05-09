from enum import Enum

import gpiozero
from gpiozero.pins.native import NativeFactory


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
