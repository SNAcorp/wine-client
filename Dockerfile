# Базовый образ
FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    uvicorn \
    curl \
    gnupg \
    lsb-release \
    libgtk-3-dev \
    libwebkit2gtk-4.0-dev \
    python3-rpi.gpio \
    python3-smbus \
    python3-spidev \
    i2c-tools \
    x11-apps \
    libmtdev-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы проекта
WORKDIR /app
COPY . /app

# Установка Python зависимостей
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install spidev RPi.GPIO smbus requests

# Установка прав на запуск основного файла
RUN chmod +x main.py

COPY . .
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Установка команд по умолчанию
CMD ["python", "main.py"]



