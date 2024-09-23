import os
import threading
import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.uix.popup import Popup

# Импортируем модули для работы с оборудованием
from modules.RFIDReader import RFIDReader
from modules.DrinkDispenser import DrinkDispenser
from modules.ButtonReader import ButtonReader
from services.Dictionaries import Dictionaries
from services.Registration import TerminalRegistration

# Инициализируем глобальные данные
registration = TerminalRegistration()
dictionaries = Dictionaries()

# URL для API запросов
API_URL_TEMPLATE = f"http://51.250.37.160/terminal/terminal-bottles/{registration.terminal_id}"
API_URL_USAGE = "http://51.250.37.160/terminal/use"
portions = {"small": 0, "big": 1}
portions_time = {}


# Функция для отправки данных о порции через API
def use_terminal_portion(portion_type: str, rfid_code: str, slot_number: int):
    try:
        response = requests.post(
            API_URL_USAGE,
            json={
                "terminal_id": registration.terminal_id,
                "token": registration.token,
                "rfid_code": rfid_code,
                "slot_number": slot_number,
                "volume": portions[portion_type]
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        print(f"Error using terminal portion: {e}")
        return None


# Функция для получения данных о бутылках через API
def fetch_bottles_data():
    try:
        response = requests.get(API_URL_TEMPLATE)
        response.raise_for_status()
        data = response.json()
        global portions_time
        portions_time = data["volumes"]
        return sorted(data['bottles'], key=lambda x: x['slot_number'])
    except requests.RequestException as e:
        print(f"Error fetching bottles data: {e}")
        return []


# Главный экран приложения
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.container = BoxLayout(orientation='vertical')
        layout.add_widget(self.container)
        self.add_widget(layout)

    def on_enter(self):
        # Очищаем контейнер и загружаем данные
        self.container.clear_widgets()
        threading.Thread(target=self.load_bottles).start()

    def load_bottles(self):
        bottles = fetch_bottles_data()
        Clock.schedule_once(lambda dt: self.display_bottles(bottles))

    def display_bottles(self, bottles):
        for bottle in bottles:
            tile = Button(text=f"{bottle['name']} ({bottle['location']})", size_hint_y=None, height=100,
                          on_press=lambda x, b=bottle: self.select_bottle(b))
            if bottle['remaining_volume'] < 120:
                tile.disabled = True
                tile.background_color = (0.5, 0.5, 0.5, 1)
            self.container.add_widget(tile)

    def select_bottle(self, bottle):
        # Переход на экран с деталями бутылки
        self.manager.current = 'details'
        details_screen = self.manager.get_screen('details')
        details_screen.display_bottle(bottle)


# Экран с деталями бутылки
class BottleDetailsScreen(Screen):
    selected_bottle = None

    def __init__(self, **kwargs):
        super(BottleDetailsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.bottle_image = AsyncImage()
        self.bottle_name = Label(text="Название")
        self.bottle_location = Label(text="Местоположение")
        self.bottle_description = Label(text="Описание")
        small_button = Button(text="Малая порция", size_hint_y=None, height=50,
                              on_press=lambda x: self.select_portion("small"))
        big_button = Button(text="Большая порция", size_hint_y=None, height=50,
                            on_press=lambda x: self.select_portion("big"))
        back_button = Button(text="Назад", size_hint_y=None, height=50, on_press=self.go_back)

        layout.add_widget(self.bottle_image)
        layout.add_widget(self.bottle_name)
        layout.add_widget(self.bottle_location)
        layout.add_widget(self.bottle_description)
        layout.add_widget(small_button)
        layout.add_widget(big_button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def display_bottle(self, bottle):
        # Устанавливаем изображение и данные бутылки
        self.selected_bottle = bottle
        image_path = f'images/{bottle["id"]}.jpg'
        if os.path.exists(image_path):
            self.bottle_image.source = image_path
        else:
            self.bottle_image.source = "https://via.placeholder.com/300x400?text=No+Image+Available"

        self.bottle_name.text = bottle['name']
        self.bottle_location.text = bottle['location']
        self.bottle_description.text = bottle['description']

    def select_portion(self, portion_type):
        threading.Thread(target=self.handle_portion, args=(portion_type,)).start()

    def handle_portion(self, portion_type):
        # Запуск процесса через RFIDReader и DrinkDispenser
        rfid_reader = RFIDReader()
        rfid_code = rfid_reader.start_reading()

        slot_number = self.selected_bottle['slot_number']
        dispenser = DrinkDispenser(slot_number, portions_time[portion_type])
        dispenser.pour()

        response = use_terminal_portion(portion_type, rfid_code, slot_number)
        if response:
            Clock.schedule_once(lambda dt: self.show_success())
        else:
            Clock.schedule_once(lambda dt: self.show_error())

    def show_success(self):
        popup = Popup(title="Успех", content=Label(text="Порция успешно выдана!"), size_hint=(0.6, 0.4))
        popup.open()

    def show_error(self):
        popup = Popup(title="Ошибка", content=Label(text="Не удалось выдать порцию."), size_hint=(0.6, 0.4))
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'main'


# Основное приложение Kivy
class WineApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(BottleDetailsScreen(name='details'))
        return sm


if __name__ == '__main__':
    WineApp().run()
