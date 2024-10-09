import RPi.GPIO as GPIO
from pirc522 import RFID
import signal
import sys

class RFIDReader:
    """Класс для работы с RFID модулем RC522"""

    def __init__(self):
        # Проверяем текущий режим и устанавливаем GPIO.BOARD, если он не установлен
        current_mode = GPIO.getmode()
        if current_mode is not None and current_mode != GPIO.BOARD:
            print(f"GPIO mode already set to {current_mode}, cleaning up.")
            GPIO.cleanup()  # Сбрасываем настройки GPIO
        elif current_mode == GPIO.BOARD:
            print(f"GPIO mode is already set to BOARD: {current_mode}")
        else:
            GPIO.setmode(GPIO.BOARD)

        # Инициализация модуля RFID
        self.rdr = RFID()

        # Захват сигнала для корректного завершения
        signal.signal(signal.SIGINT, self.cleanup)

    def cleanup(self, signum=None, frame=None):
        """ Очистка и завершение программы """
        print("Завершение программы...")
        self.rdr.cleanup()
        GPIO.cleanup()  # Сброс GPIO
        sys.exit()

    def start_reading(self):
        """Основная функция для считывания меток RFID"""
        while True:
            self.rdr.wait_for_tag()
            (error, tag_type) = self.rdr.request()
            if not error:
                print("Метка найдена!")
                (error, uid) = self.rdr.anticoll()
                if not error:
                    return str(uid)

