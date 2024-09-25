FROM balenalib/raspberrypi3-python:3.9-bullseye

# Установка основных системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    uvicorn \
    curl \
    gnupg \
    lsb-release \
    libgtk-3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    xclip \
    xsel \
    git \
    ffmpeg \
    libsdl2-ttf-2.0-0 \
    pkg-config \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    mesa-common-dev \
    python3-dev \
    libwebkit2gtk-4.0-dev \
    python3-rpi.gpio \
    python3-smbus \
    python3-spidev \
    i2c-tools \
    x11-apps \
    libmtdev-dev \
    libgl1-mesa-glx \
    libgles2-mesa \
    python3-pip \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка необходимых Python-зависимостей
RUN pip install --upgrade pip setuptools wheel

# Установка зависимостей Kivy
RUN pip install cython kivy kivymd

# Установка дополнительных зависимостей
RUN pip install spidev RPi.GPIO smbus requests Pillow

# Установка pygame (используем предварительно скомпилированные колеса, если доступны)
RUN pip install pygame

# Копирование приложения в контейнер
WORKDIR /app
COPY . /app

# Установка зависимостей приложения
RUN pip install --no-cache-dir -r requirements.txt

# Установка прав на выполнение скрипта
RUN chmod +x main.py

# Команда запуска приложения
CMD ["python", "main.py"]




