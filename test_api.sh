#!/bin/bash

echo "Тестирование Office Reservation API..."
echo ""

BASE_URL="http://localhost:8000"

echo "1️ Health check..."
curl -s "$BASE_URL/" | python3 -m json.tool
echo ""
echo ""

echo "2️ Получение списка офисов..."
curl -s "$BASE_URL/api/offices" | python3 -m json.tool
echo ""
echo ""

echo "3 Проверка доступности офиса..."
curl -s -X POST "$BASE_URL/api/offices/availability" \
  -H "Content-Type: application/json" \
  -d '{
    "office_id": 1,
    "date": "2025-12-05",
    "start_time": "09:00",
    "end_time": "10:00"
  }' | python3 -m json.tool
echo ""
echo ""

echo "4️ Создание бронирования..."
curl -s -X POST "$BASE_URL/api/reservations" \
  -H "Content-Type: application/json" \
  -d '{
    "office_id": 2,
    "name": "Фарход Раҳимов",
    "email": "farhod.rahimov@mail.tj",
    "phone": "+992927654321",
    "date": "2025-12-06",
    "start_time": "10:00",
    "end_time": "11:00"
  }' | python3 -m json.tool
echo ""
echo ""

echo "Тестирование завершено!"
echo "Откройте Swagger UI: http://localhost:8000/docs"
