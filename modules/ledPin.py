import board
import busio
import time
from adafruit_pca9685 import PCA9685


# Класс управления светодиодами
class LedController:
    def __init__(self, address: int, channel: int, frequency: int = 500):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c, address=address)
        self.pca.frequency = frequency
        self.channel = self.pca.channels[channel]

    def fade_in(self, steps: int = 4096, delay: float = 0.001):
        for i in range(steps):
            self.channel.duty_cycle = int(i * 65535 / steps)
            time.sleep(delay)

    def fade_out(self, steps: int = 4096, delay: float = 0.001):
        for i in range(steps, -1, -1):
            self.channel.duty_cycle = int(i * 65535 / steps)
            time.sleep(delay)

    def turn_off(self):
        self.channel.duty_cycle = 0

    def turn_on(self, brightness: float = 1.0):
        self.channel.duty_cycle = int(65535 * brightness)

    def deinit(self):
        self.pca.deinit()
