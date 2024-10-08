
class Storage:

    """В данный момент I2C под номером 0x22 не существует,
     в дальнейшем планируется использовать её для кнопок
     и подсветки (сборки из четырёх бутылок)"""

    __led_bottle = {0: (0x23, 0), 1: (0x23, 1), 2: (0x23, 2), 3: (0x23, 3),
                    4: (0x23, 4), 5: (0x22, 3), 6: (0x23, 6), 7: (0x23, 7)}


    """ Пины для управления насосами (диспенсером) """
    __pump_Pin = {0: (0x20, 0), 1: (0x20, 1), 2: (0x20, 2), 3: (0x20, 3),
                  4: (0x20, 4), 5: (0x20, 5), 6: (0x20, 6), 7: (0x20, 7)}

    # Программа не учитывает нажатие на кнопку.
    # Настроить выборку значения для wait_for_button_press
    # доработать отчищение пинов и вообщем всей программы после завершениия

    """Ссылка на сервер"""
    __server_url = "http://localhost"

    """Путь к файлу с логами основного цикла программы"""
    __path_to_log_file = "technical_information/log.json"

    """Путь к файлу с регистрационной информацией о терминале"""
    __path_to_tech_file = "technical_information/terminal_info.json"

    """Путь к файлу с логами времени работы всей программы"""
    __path_to_system_file = "technical_information/system_info.json"

    """Путь к временному хранилищу данных при обрыве связи с сервером"""
    __path_to_swap_file = "technical_information/swap.json"

    """Ссылка для регистрации терминала"""
    __link_for_registration = "http://localhost/terminal/register-terminal"

    """Ссылка для контроля состояния сервера в сети"""
    __link_for_session_control = "https://wine.mag.tc"

    """Ссылка для проверки rfid меток"""
    __link_for_rfid = "http://rfid/validate/{rfid_code}"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance
    
    #     def __init__(self):
    # #         self.clean()
    #         self.setup()
    # def clean(self):
    #     self.__clean_pins(list(self.__pump_Pin.values()))
    #     self.__clean_pins(list(self.__button_Pin.values()))
    #     self.__clean_pins(list(self.__button_Pin_led.values()))
    #     self.__clean_pins(list(self.__led_bottle.values()))
    #
    # def __clean_pins(self, lst: list):
    #     for element in lst:
    #         element.clear()

    # def setup(self):
    #     self.__setup_pins(list(self.__pump_Pin.values()), "output")
    #     self.__setup_pins(list(self.__button_Pin.values()), "input")
    #     self.__setup_pins(list(self.__button_Pin_led.values()), "output")
    #     self.__setup_pins(list(self.__led_bottle.values()), "output")
    # def __setup_pins(self, lst: list, status: str) -> None:
    #     for element in lst:
    #         element.set_mode(status)

    @property
    def get_log_file_path(self) -> str:
        """
        Возвращаем путь к файлу с логами
        """
        return self.__path_to_log_file

    @property
    def get_swap_file_path(self) -> str:
        """
        Возвращаем путь к файлу swap'a
        """
        return self.__path_to_swap_file
    
    @property
    def get_system_log_file_path(self):
        """
        Возвращаем путь к файлу с логами циклов перезапуска программы
        """
        return self.__path_to_system_file

    @property
    def get_link_for_registration(self) -> str:
        """
        Возвращаем ссылку на api регистрации в с системе
        """
        return self.__link_for_registration

    @property
    def get_link_for_session_control(self) -> str:
        """
        Возвращаем ссылку на api регистрации в с системе
        """
        return self.__link_for_session_control

    @property
    def get_tech_file_path(self) -> str:
        """
        Возвращаем путь к файлу с технической информацией
        """
        return self.__path_to_tech_file

    def dispander_pin(self, number_of_bottle: int):
        """
        Возвращаем номер пина нужного нам насоса
        """
        return self.__pump_Pin.get(number_of_bottle)



    @property
    def server_url(self) -> str:
        """
        Получение ссылки на сервер
        """
        return self.__server_url

    @property
    def rfid_url(self) -> str:
        """
        Получение ссылки на сервер проверки rfid
        """
        return self.__link_for_rfid


