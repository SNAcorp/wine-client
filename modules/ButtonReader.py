from storage.Storage import Storage
from modules.Pin import Pin, PinMode
from modules.DrinkDispenser import DrinkDispenser

class ButtonReader:
    """Класс для чтения состояния кнопок и управления процессом"""

    def __init__(self, pin: Pin, slot_number: int):
        self.storage = Storage()
        self.storage.turn_off_all_leds()
        self.__run = True

        button_address, button_pin = self.storage.button_pin(slot_number)


        pin.set_mode(PinMode.INPUT)
        self.button_pin = Pin(button_address, button_pin)
        self.button_pin.set_mode(PinMode.INPUT)
        self.button_pin.wait_for_press()
        pin.set_mode(PinMode.OUTPUT)