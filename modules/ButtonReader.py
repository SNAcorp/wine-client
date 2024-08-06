from storage.Storage import Storage
from modules.Pin import Pin, PinMode
from modules.DrinkDispenser import DrinkDispenser

class ButtonReader:
    """Класс для чтения состояния кнопок и управления процессом"""

    def __init__(self, leds: list, slot_number: int):
        self.storage = Storage()
        self.storage.turn_off_all_leds()
        self.__run = True

        pin = next((led for led in leds if led.pin_number == slot_number), None)
        print("good")
        if pin is None:
            raise ValueError(f"No LED found for slot number {slot_number}")

        button_address, button_pin = self.storage.button_pin(slot_number)

        pin.set_mode(PinMode.INPUT)
        self.button_pin = Pin(button_address, button_pin)
        self.button_pin.set_mode(PinMode.INPUT)
        self.button_pin.wait_for_press()
        pin.set_mode(PinMode.OUTPUT)
        print("very good")