# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем зависимости через apt
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    gnupg \
    lsb-release \
    libgtk-3-dev \
    libwebkit2gtk-4.0-dev \
    python3-dev \
    python3-spidev \
    python3-smbus \
    i2c-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-зависимости (включая RPi.GPIO)
RUN pip install RPi.GPIO smbus spidev uvicorn requests
RUN pip install adafruit-circuitpython-pca9685 adafruit-blinka

# Копируем файл с зависимостями
COPY requirements.txt .

# Скрипт для повторных попыток установки зависимостей
RUN echo '#!/bin/sh\n\
n=0\n\
until [ "$n" -ge 5 ]\n\
do\n\
   pip install --no-cache-dir -r requirements.txt && break\n\
   n=$((n+1))\n\
   sleep 5\n\
done' > install_requirements.sh \
    && chmod +x install_requirements.sh \
    && ./install_requirements.sh

# Копируем файлы проекта
COPY . .
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

EXPOSE 80

# Команда для запуска приложения
CMD ["/bin/bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 80"]
