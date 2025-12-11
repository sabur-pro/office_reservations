@echo off
echo Запуск Office Reservation API сервера...
echo.

if not exist ".venv" (
    echo Виртуальное окружение не найдено. Создаю...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Проверка зависимостей...
python -c "import sqlalchemy" 2>NUL
if %errorlevel% neq 0 (
    echo Установка зависимостей...
    pip install -r requirements.txt
)
echo Зависимости OK
echo.

if not exist ".env" (
    echo Создание файла .env...
    copy .env.example .env
)

echo Запуск сервера...
echo (Убедитесь, что Postgres и Redis запущены, или используйте Docker)

REM Принудительно используем localhost
set DATABASE_URL=postgresql://office_user:123456@localhost:5433/office_reservations
set REDIS_URL=redis://localhost:6379/0

echo DEBUG: DATABASE_URL is %DATABASE_URL%
echo DEBUG: REDIS_URL is %REDIS_URL%

echo Запуск сервера...
python app.py
pause
