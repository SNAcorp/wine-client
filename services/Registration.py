from storage.Storage import Storage
import requests
import json
import os
import time


class TerminalRegistration:
    """ Описание класса """

    def __init__(self):
        """Attributes:
            self.ath (str): Путь к файлу.
            self.link (str): Ссылка для регистрации.
            self.__info (dict): Информация о терминале.
        """
        self.path = Storage().get_tech_file_path
        self.link = "http://51.250.89.99/terminal/register-terminal"
        self.__info = {}
        self.__load_terminal_info()

    def __load_terminal_info(self):
        """
        Загружает информацию о терминале из файла или регистрирует новый терминал.

        Returns:
            tuple: Кортеж с ID и именем терминала.
        """
        if os.path.exists(self.path):
            with open(self.path, 'r') as file:
                self.__info = json.load(file)
                # serial = self.__get_serial_number()
                # if self.__info['serial'] != serial:
                #     response = requests.post('api',
                #                              json={'token': self.__info['token'],
                #                                    "serial": serial})
                #     if response.status_code == 200:
                #         self.__info['token'] = response.json()['jwt']
                #         self.__info['serial'] = serial
                #         self.__save_terminal_info()
        else:
            self.__register_terminal()

    def __register_terminal(self):
        """
        Регистрирует новый терминал.

        Returns:
            tuple: Кортеж с ID и именем зарегистрированного терминала.
        """
        serial = "1234567"
        while True:
            response = requests.post(self.link, json={"serial": serial})
            if response.status_code == 200:
                self.__info = {'id': response.json()['terminal_id'],
                               'serial': serial,
                               'token': response.json()['token']}

                self.__save_terminal_info()
                break
            else:
                time.sleep(1)

    def __save_terminal_info(self):
        """
        Сохраняет ID терминала в файл.

        Args:
            self.terminal_id (str): ID терминала.
            self.token (str): Token терминала.
            self.terminal_serial (str): Серийный номер терминала.

        Returns:
            None
        """
        dir_name = os.path.dirname(self.path)
        os.makedirs(dir_name, exist_ok=True)
        with open(self.path, 'w+') as file:
            json.dump(self.__info, file)

    @staticmethod
    def __get_serial_number():
        """ Описание функции """
        serial_number = None
        try:
            # Открываем файл /proc/cpuinfo
            with open('/proc/cpuinfo', 'r') as file:
                # Читаем все содержимое файла
                cpuinfo = file.read()
                # Находим индекс начала строки с серийным номером
                start_index = cpuinfo.find('Serial')
                if start_index != -1:
                    # Находим конец строки с серийным номером
                    end_index = cpuinfo.find('\n', start_index)
                    # Извлекаем строку с серийным номером и убираем лишние пробелы
                    serial_number = cpuinfo[start_index:end_index].split(':')[1].strip()
        except FileNotFoundError:
            print("Файл /proc/cpuinfo не найден.")
        return serial_number

    @property
    def terminal_id(self):
        """ Описание функции """
        return self.__info['id']

    @property
    def token(self):
        """ Описание функции """
        return self.__info['token']
