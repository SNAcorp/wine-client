import RPi.GPIO as GPIO
from pirc522 import RFID
import signal
import time
import sys

class RFIDReader:
    def __init__(self):
        # Устанавливаем режим BCM для GPIO
        GPIO.setmode(GPIO.BCM)

        # Инициализация модуля RFID RC522
        self.rdr = RFID()

        # Флаг для работы
        self.run = True

        # Захват сигнала для корректного завершения
        signal.signal(signal.SIGINT, self.cleanup)

    def cleanup(self, signum=None, frame=None):
        """ Корректная очистка GPIO и завершение программы """
        print("Завершение программы...")
        self.run = False
        self.rdr.cleanup()
        GPIO.cleanup()
        sys.exit()

    @staticmethod
    def reformat_uid(uid):
        """ Преобразование UID в строку для удобного отображения """
        return "".join([format(x, '02X') for x in uid])

    def start_reading(self):
        """ Основная функция для считывания меток RFID """
        print("Ожидание метки RFID...")
        while self.run:
            # Ожидание метки
            self.rdr.wait_for_tag()

            # Чтение данных с метки
            (error, tag_type) = self.rdr.request()
            if not error:
                print("Метка найдена!")

                # Считывание UID
                (error, uid) = self.rdr.anticoll()
                if not error:
                    uid_str = self.reformat_uid(uid)
                    return uid_str
