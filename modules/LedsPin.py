import smbus
from storage.Storage import Storage
from modules.Pin import Pin, PinMode


class ButtonLightController:
    """Класс для управления подсветкой кнопок с использованием smbus"""

    def __init__(self, i2c_bus: int, leds: list):
        self.bus = smbus.SMBus(i2c_bus)  # инициализация I2C-шины
        self.storage = Storage()
        self.leds = leds

    def turn_on_led(self, slot_number: int):
        """Включает подсветку для кнопки с указанным слотом"""
        pin = next((led for led in self.leds if led.pin_number == slot_number), None)
        if pin is None:
            raise ValueError(f"No LED found for slot number {slot_number}")

        button_address, _ = self.storage.button_pin(slot_number)
        pin.set_mode(PinMode.OUTPUT)
        self.bus.write_byte(button_address, 0xFF)  # Включаем подсветку (предполагая, что 0xFF включает светодиод)

    def turn_off_led(self, slot_number: int):
        """Выключает подсветку для кнопки с указанным слотом"""
        pin = next((led for led in self.leds if led.pin_number == slot_number), None)
        if pin is None:
            raise ValueError(f"No LED found for slot number {slot_number}")

        button_address, _ = self.storage.button_pin(slot_number)
        pin.set_mode(PinMode.OUTPUT)
        self.bus.write_byte(button_address, 0x00)  # Выключаем подсветку (предполагая, что 0x00 выключает светодиод)

    def turn_off_all_leds(self):
        """Выключает подсветку для всех кнопок"""
        for pin in self.leds:
            button_address, _ = self.storage.button_pin(pin.pin_number)
            pin.set_mode(PinMode.OUTPUT)
            self.bus.write_byte(button_address, 0x00)  # Выключаем подсветку для каждого светодиода

