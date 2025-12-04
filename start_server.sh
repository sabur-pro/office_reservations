#!/bin/bash

echo "Запуск Office Reservation API сервера..."
echo ""

if [ ! -d ".venv" ]; then
    echo "Виртуальное окружение не найдено"
    echo "Создайте его командой: python3 -m venv .venv"
    exit 1
fi

source .venv/bin/activate

if ! python3 -c "import sqlalchemy" 2>/dev/null; then
    echo "Установка зависимостей..."
    pip install -r requirements.txt
fi

echo "Зависимости установлены"
echo ""

echo "Проверка порта 8000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "Порт 8000 занят. Останавливаю старый процесс..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

python3 app.py

