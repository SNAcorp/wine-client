from storage.Storage import Storage
from modules.Pin import Pin, PinMode
from modules.DrinkDispenser import DrinkDispenser
from modules.LedsPin import ButtonLightController

class ButtonReader:
    """Класс для чтения состояния кнопок и управления процессом"""

    def __init__(self, slot_number: int, button_light_controller: ButtonLightController):
        self.storage = Storage()
        self.__run = True

        # Получаем адреса и пины для светодиода и кнопки
        led_address, led_pin = self.storage.led_pin(slot_number)
        button_address, button_pin = self.storage.button_pin(slot_number)

        # Инициализируем пины
        self.led_pin = Pin(led_address, led_pin)
        self.button_pin = Pin(button_address, button_pin)

        # Используем ButtonLightController для управления подсветкой
        self.button_light_controller = button_light_controller
        self.button_light_controller.turn_on_led(slot_number)  # Включаем подсветку

        # Устанавливаем режимы пинов
        self.led_pin.set_mode(PinMode.OUTPUT)
        self.button_pin.set_mode(PinMode.INPUT)

        # Ожидаем нажатия кнопки
        self.button_pin.wait_for_press()

        # После нажатия кнопки выключаем подсветку
        self.button_light_controller.turn_off_led(slot_number)
