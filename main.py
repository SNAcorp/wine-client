# Импорт необходимых модулей
from kivymd.app import MDApp
from kivymd.uix.spinner import MDSpinner
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from threading import Thread
import requests


# Определение экранов
class MainScreen(Screen):
    pass


class BottleDetailScreen(Screen):
    pass


class RFIDScreen(Screen):
    pass


class ButtonPressScreen(Screen):
    pass


class SuccessScreen(Screen):
    pass


# KV код с использованием KivyMD виджетов
KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import dp kivy.metrics.dp

ScreenManager:
    transition: FadeTransition()
    MainScreen:
    BottleDetailScreen:
    RFIDScreen:
    ButtonPressScreen:
    SuccessScreen

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: timer_label
            text: ''
            size_hint_y: None
            height: dp(30)
            color: 1, 0, 0, 1
            halign: 'right'
            valign: 'middle'
        ScrollView:
            GridLayout:
                id: bottle_grid
                cols: 4
                size_hint_y: None
                height: self.minimum_height
                row_default_height: dp(200)
                row_force_default: True
                spacing: dp(10)
                padding: dp(10)

<BottleTile@Button>:
    bottle_data: {}
    background_normal: ''
    background_color: (1, 1, 1, 1) if self.bottle_data['remaining_volume'] >= 120 else (0.8, 0.8, 0.8, 1)
    disabled: False if self.bottle_data['remaining_volume'] >= 120 else True
    on_press: app.select_bottle(self.bottle_data)
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        Image:
            source: self.bottle_data['image_url']
            allow_stretch: True
            keep_ratio: True
        Label:
            text: self.bottle_data['name']
            size_hint_y: None
            height: self.texture_size[1]
            halign: 'center'
            valign: 'middle'
            text_size: self.width, None
        Label:
            text: self.bottle_data['location']
            size_hint_y: None
            height: self.texture_size[1]
            font_size: '14sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.width, None

<BottleDetailScreen>:
    name: 'detail'
    BoxLayout:
        orientation: 'vertical'
        ScrollView:
            GridLayout:
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: dp(10)
                spacing: dp(10)
                AsyncImage:
                    id: bottle_image
                    source: ''
                    size_hint_y: None
                    height: dp(300)
                Label:
                    id: bottle_name
                    text: ''
                    font_size: '24sp'
                    size_hint_y: None
                    height: self.texture_size[1]
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.width, None
                Label:
                    id: bottle_location
                    text: ''
                    font_size: '18sp'
                    size_hint_y: None
                    height: self.texture_size[1]
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.width, None
                Label:
                    id: bottle_description
                    text: ''
                    font_size: '16sp'
                    size_hint_y: None
                    height: self.texture_size[1]
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.width, None
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            spacing: dp(10)
            padding: dp(10)
            Button:
                text: 'Тестовая порция'
                on_press: app.select_portion('small')
            Button:
                text: 'Полная порция'
                on_press: app.select_portion('big')
            Button:
                text: 'Назад'
                on_press: app.reset_progress()

<RFIDScreen>:
    name: 'rfid'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        Label:
            text: 'Приложите RFID метку'
            font_size: '24sp'
            halign: 'center'
            valign: 'middle'
            size_hint_y: None
            height: dp(50)
        MDSpinner:
            size_hint: None, None
            size: dp(50), dp(50)
            pos_hint: {'center_x': 0.5}
            determinate: False

<ButtonPressScreen>:
    name: 'button_press'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        Label:
            text: 'Нажмите подсвеченную кнопку для завершения операции'
            font_size: '24sp'
            halign: 'center'
            valign: 'middle'
            size_hint_y: None
            height: dp(50)
        Button:
            text: 'Завершить операцию'
            on_press: app.complete_operation()

<SuccessScreen>:
    name: 'success'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        Label:
            text: 'Операция успешно выполнена!'
            font_size: '24sp'
            halign: 'center'
            valign: 'middle'
            size_hint_y: None
            height: dp(50)
        Button:
            text: 'Вернуться в главное меню'
            on_press: app.reset_progress()
'''


# Главный класс приложения
class WineApp(MDApp):
    def build(self):
        self.title = 'WineTech'
        self.icon = 'icon.png'  # Замените на путь к иконке вашего приложения
        self.sm = Builder.load_string(KV)
        self.bottles = []
        self.selected_bottle = None
        self.rfid_code = None
        self.portion_type = None
        self.portions_time = {}
        self.time_left = 60
        self.countdown_event = None

        self.load_bottles_data()
        return self.sm

    def load_bottles_data(self):
        try:
            # Замените на ваш реальный URL для получения данных
            API_URL = f'http://51.250.89.99/terminal/terminal-bottles/YOUR_TERMINAL_ID'
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()
            self.bottles = data['bottles']
            self.portions_time = data['volumes']
            self.populate_menu()
        except requests.RequestException as e:
            print(f"Ошибка при загрузке данных: {e}")
            self.show_error_popup("Ошибка при загрузке данных. Проверьте соединение.")

    def populate_menu(self):
        main_screen = self.sm.get_screen('main')
        bottle_grid = main_screen.ids.bottle_grid
        bottle_grid.clear_widgets()
        for bottle in self.bottles:
            bottle_data = {
                'id': bottle['id'],
                'name': bottle['name'],
                'location': bottle['location'].replace('\n', ' · '),
                'description': bottle['description'],
                'image_url': f"http://51.250.89.99/bottles/image/{bottle['id']}/300",
                'slot_number': bottle['slot_number'],
                'remaining_volume': bottle['remaining_volume']
            }
            tile = Builder.template('BottleTile', bottle_data=bottle_data)
            bottle_grid.add_widget(tile)

    def select_bottle(self, bottle_data):
        self.selected_bottle = bottle_data
        detail_screen = self.sm.get_screen('detail')
        detail_screen.ids.bottle_image.source = f"http://51.250.89.99/bottles/image/{bottle_data['id']}/600"
        detail_screen.ids.bottle_name.text = bottle_data['name']
        detail_screen.ids.bottle_location.text = bottle_data['location']
        detail_screen.ids.bottle_description.text = bottle_data['description']
        self.sm.current = 'detail'
        self.start_timer()

    def select_portion(self, portion_type):
        self.portion_type = portion_type
        self.sm.current = 'rfid'
        Thread(target=self.read_rfid).start()

    def read_rfid(self):
        # Ваш код для чтения RFID
        try:
            from modules.RFIDReader import RFIDReader
            rfid_reader = RFIDReader()
            result = rfid_reader.start_reading()
            if not result['is_valid']:
                self.show_error_popup('Невалидный RFID')
            else:
                self.rfid_code = result['rfid_code']
                self.sm.current = 'button_press'
        except Exception as e:
            print(f"Ошибка при чтении RFID: {e}")
            self.show_error_popup('Ошибка при чтении RFID')

    def complete_operation(self):
        # Ваш код для завершения операции
        try:
            from modules.ButtonReader import ButtonReader
            from modules.DrinkDispenser import DrinkDispenser

            ButtonReader(self.selected_bottle['slot_number'])
            DrinkDispenser(self.selected_bottle['slot_number'], self.portions_time[self.portion_type])

            # Отправка данных об использовании терминала
            API_URL_USAGE = 'http://51.250.89.99/terminal/use'
            payload = {
                "terminal_id": 'YOUR_TERMINAL_ID',
                "token": 'YOUR_TOKEN',
                "rfid_code": self.rfid_code,
                "slot_number": self.selected_bottle['slot_number'],
                "volume": self.portion_type
            }
            response = requests.post(API_URL_USAGE, json=payload)
            if response.status_code == 200:
                self.sm.current = 'success'
            else:
                self.show_error_popup('Доступ запрещён или лимит превышен.')
        except Exception as e:
            print(f"Ошибка при завершении операции: {e}")
            self.show_error_popup('Ошибка при завершении операции')

    def reset_progress(self):
        self.selected_bottle = None
        self.rfid_code = None
        self.portion_type = None
        self.stop_timer()
        self.sm.current = 'main'

    def show_error_popup(self, message):
        popup = Popup(title='Ошибка',
                      content=Label(text=message),
                      size_hint=(0.8, 0.3))
        popup.open()
        self.reset_progress()

    def start_timer(self):
        self.time_left = 60
        self.update_timer_label()
        self.countdown_event = Clock.schedule_interval(self.update_timer, 1)

    def stop_timer(self):
        if self.countdown_event:
            self.countdown_event.cancel()
            self.sm.get_screen('main').ids.timer_label.text = ''

    def update_timer(self, dt):
        self.time_left -= 1
        self.update_timer_label()
        if self.time_left <= 0:
            self.stop_timer()
            self.reset_progress()

    def update_timer_label(self):
        timer_label = self.sm.get_screen('main').ids.timer_label
        timer_label.text = f'Осталось времени: {self.time_left} сек'


if __name__ == '__main__':
    WineApp().run()
