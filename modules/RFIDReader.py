import RPi.GPIO as GPIO
from pirc522.rfid import RFID
from services.Dictionaries import Dictionaries
import requests
import signal
import sys
import datetime


class RFIDReader:
    """Класс для работы с RFID-модулем RC522"""

    def __init__(self):
        self.run = True

        # Устанавливаем GPIO режим BCM
        current_mode = GPIO.getmode()
        if current_mode is not None and current_mode != GPIO.BCM:
            print(f"GPIO mode already set to {current_mode}, cleaning up.")
            GPIO.cleanup()  # Сброс настроек GPIO
        elif current_mode == GPIO.BCM:
            print(f"GPIO mode is already set to BCM: {current_mode}")
        else:
            print("Setting GPIO mode to BCM")
            GPIO.setmode(GPIO.BCM)

        # Инициализация RFID-модуля
        self.rdr = RFID()
        self.util = self.rdr.util()
        self.util.debug = True

        # Инициализация словарей
        self.dictionaries = Dictionaries()

        # Обработка сигнала SIGINT для корректного завершения работы
        signal.signal(signal.SIGINT, self.clean)

    """Функция для корректного завершения чтения RFID"""

    def clean(self, signum=None, frame=None):
        self.run = False
        self.rdr.cleanup()
        GPIO.cleanup()  # Очищаем GPIO перед завершением
        sys.exit()

    """Преобразование UID из списка в строку"""

    @staticmethod
    def reformat_uid(uid):
        result = "".join([str(number) for number in uid])
        return result

    """Отправка UID на сервер"""

    @staticmethod
    def send_to_server(uid) -> dict:
        # Пример для отправки на сервер (закомментировано)
        # server_url = f"http://localhost/rfid/validate/{uid}"
        # response = requests.get(server_url)
        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     return {"status": "broken"}
        return {'access_granted': "granted"}

    """Основная функция для считывания меток"""

    def start_reading(self):
        while self.run:
            # Ожидаем появления метки
            self.rdr.wait_for_tag()

            # Читаем данные с метки
            (error, data) = self.rdr.request()
            if not error:
                print("\nDetected tag with data: " + format(data, "02x"))

            # Избегаем коллизий при считывании
            (error, uid) = self.rdr.anticoll()

            # Если нет ошибок, обрабатываем UID
            if not error and uid is not None:
                # Форматируем UID в строку
                uid_str = self.reformat_uid(uid)
                print("UID: " + uid_str)

                # Отправляем UID на сервер (можно раскомментировать при необходимости)
                # response = self.send_to_server(uid_str)
                # response["rfid_code"] = uid_str

                # Возвращаем UID для дальнейшего использования
                return uid_str
