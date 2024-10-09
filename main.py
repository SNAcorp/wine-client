import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from modules.DrinkDispenser import DrinkDispenser
from modules.RFIDReader import RFIDReader
from modules.ledPin import LedController
import RPi.GPIO as GPIO
app = FastAPI()

portions = {"small": 3, "big": 9}


@app.post("/rfid", response_class=JSONResponse)
async def rfid() -> dict:
    GPIO.setmode(GPIO.BOARD)
    rfid_reader = RFIDReader()
    result = rfid_reader.start_reading()
    return {"rfid_code": result}


# 352481425297
@app.post("/dispanser", response_class=JSONResponse)
async def portion(request: Request):
    data = await request.json()
    slot_num, portion_type = data["slot_number"], data["portion_type"]
    DrinkDispenser(slot_num, portions[portion_type])

    return {"success": True}

@app.post("/led/{num}", response_class=JSONResponse)
async def portion(request: Request, num: int):

    # Управляем светодиодом на 0 канале с адресом 0x40
    led = LedController(address=0x40, channel=num)

    led.fade_in(steps=100, delay=0.05)  # Плавное включение
    time.sleep(1)
    led.fade_out(steps=100, delay=0.05)  # Плавное выключение
    time.sleep(1)

    return {"success": True}




if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
