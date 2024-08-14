from storage.Storage import Storage
from modules.Pin import Pin, PinMode
from modules.LedPumpPin import LedPumpPin
import time


class DrinkDispenser:

    def __init__(self, slot_number: int, volume: float):

        self.storage = Storage()
        print("жижа")
        pump_address, pump_pin_number = self.storage.dispander_pin(slot_number)
        self.pump_pin = Pin(pump_address, pump_pin_number)
        self.pump_pin.set_mode(PinMode.INPUT)
        print("Куралес")
        time.sleep(volume)
        self.pump_pin.set_mode(PinMode.OUTPUT)
        print("знающий")
