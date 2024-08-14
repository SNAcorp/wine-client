from storage.Storage import Storage
from modules.Pin import Pin, PinMode
from modules.DrinkDispenser import DrinkDispenser
from modules.LedsPin import ButtonLightController  # Импортируем новый класс

class ButtonReader:
    """Класс для чтения состояния кнопок и управления процессом"""

    def __init__(self, leds: list, slot_number: int, button_light_controller: ButtonLightController):
        self.storage = Storage()
        self.__run = True

        # Ищем соответствующий Pin по номеру слота
        pin = next((led for led in leds if led.pin_number == slot_number), None)
        if pin is None:
            raise ValueError(f"No LED found for slot number {slot_number}")

        # Получаем адрес и пин кнопки
        button_address, button_pin = self.storage.button_pin(slot_number)

        # Настраиваем режимы пинов
        pin.set_mode(PinMode.INPUT)
        self.button_pin = Pin(button_address, button_pin)
        self.button_pin.set_mode(PinMode.INPUT)

        # Управляем подсветкой с помощью ButtonLightController
        self.button_light_controller = button_light_controller
        self.button_light_controller.turn_on_led(slot_number)  # Включаем подсветку

        # Ожидаем нажатия кнопки
        self.button_pin.wait_for_press()

        # После нажатия кнопки выключаем подсветку
        self.button_light_controller.turn_off_led(slot_number)

        # Настраиваем пин обратно на вывод
        pin.set_mode(PinMode.OUTPUT)
