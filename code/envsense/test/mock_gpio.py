import gpiozero
import gpiozero.pins.mock


class PinState:
    def __init__(self, state):
        self.value = state


class MockGPIO(object):
    pinStates = dict()

    def __init__(self, number: int, direction):
        assert 0 <= number <= 27
        gpiozero.Device.pin_factory = gpiozero.pins.mock.MockFactory()

        if number not in MockGPIO.pinStates:
            new_pin = PinState(0)
            MockGPIO.pinStates[number] = self.pin = new_pin
        else:
            self.pin = MockGPIO.pinStates[number]
