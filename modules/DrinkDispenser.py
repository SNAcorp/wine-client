from storage.Storage import Storage
from modules.Pin import PumpPin, PinMode
import time


class DrinkDispenser:

    def __init__(self, slot_number: int, volume: float):
        self.storage = Storage()

        pump_address, pump_pin_number = self.storage.dispander_pin(slot_number)
        pump_pin = PumpPin(pump_address, pump_pin_number)
        pump_pin.write(0x00)
        time.sleep(volume)
        pump_pin.write(0xFF)
