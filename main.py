from threading import Thread
from fastapi.templating import Jinja2Templates
import requests
import uvicorn
import webview
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from modules.DrinkDispenser import DrinkDispenser
from modules.RFIDReader import RFIDReader
from modules.ButtonReader import ButtonReader
from modules.LedPumpPin import LedPumpPin
from services.Dictionaries import Dictionaries
from services.Registration import TerminalRegistration

registration = TerminalRegistration()
dictionaries = Dictionaries()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_URL_TEMPLATE = f"http://51.250.89.99/terminal/terminal-bottles/{registration.terminal_id}"
API_URL_REGISTRATION = "http://51.250.89.99/terminal/register-terminal"
API_URL_USAGE = "http://51.250.89.99/terminal/use"
portions = {"small": 0, "big": 1}
portions_time = {}


def use_terminal_portion(portion_type: str, rfid_code: str, slot_number: int):
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


def fetch_bottles_data():
    try:
        response = requests.get(API_URL_TEMPLATE)
        response.raise_for_status()
        print(response.status_code)
        data = response.json()
        print(data)
        global portions_time
        portions_time = data["volumes"]
        return sorted(data['bottles'], key=lambda x: x['slot_number'])
    except requests.RequestException as e:
        print(f"Error fetching bottles data: {e}")
        return []


@app.post("/rfid", response_class=JSONResponse)
async def rfid() -> dict:
    rfid_reader = RFIDReader()
    result = rfid_reader.start_reading()
    print(result)
    return result


# 352481425297
@app.post("/button", response_class=JSONResponse)
async def portion(request: Request):
    data = await request.json()
    print(data.keys())
    slot_num, portion_type, rfid_code = data["slot_number"], data["portion_type"], data["rfid"]
    ButtonReader(slot_num)
    DrinkDispenser(slot_num, portions_time[portion_type])
    response = use_terminal_portion(portion_type, rfid_code, slot_num)
    bottles = fetch_bottles_data()
    return {"success": True}


@app.get("/", response_class=JSONResponse)
async def get_bottles(request: Request):
    bottles = fetch_bottles_data()
    return templates.TemplateResponse("index.html", {"request": request, "bottles": bottles})


@app.get("/bottle/{slot_number}", response_class=JSONResponse)
async def get_bottle_detail(request: Request, slot_number: int):
    bottles = fetch_bottles_data()
    bottle = next((b for b in bottles if b['slot_number'] == slot_number), None)
    return bottle


def open_browser():
    webview.create_window("WineTech", "http://127.0.0.1:8000", fullscreen=True)
    webview.start()


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == '__main__':

    LedPin.turn_of_all_leds()
    # Запуск сервера в отдельном потоке
    server_thread = Thread(target=start_server)
    server_thread.start()

    # Запуск браузера в полноэкранном режиме
    webview.create_window("Wine App", "http://localhost:8000", fullscreen=True, text_select=False)
    webview.start()
