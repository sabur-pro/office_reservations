#!/bin/bash

echo "=========================================="
echo "Office Reservation System - Test Suite"
echo "=========================================="
echo ""

echo "Test 1: Check availability (should be free)"
echo "Command: python3 main.py check-availability --office-id 1 --date 2025-12-05 --start-time 10:00 --end-time 12:00"
python3 main.py check-availability --office-id 1 --date 2025-12-05 --start-time 10:00 --end-time 12:00
echo ""
echo "Press Enter to continue..."
read

echo "=========================================="
echo "Test 2: Book office 1"
echo "Command: python3 main.py book --office-id 1 --date 2025-12-05 --start-time 10:00 --end-time 12:00 --name 'Farrukh Rahimov' --email 'farrukh@example.tj' --phone '+992901234567'"
python3 main.py book --office-id 1 --date 2025-12-05 --start-time 10:00 --end-time 12:00 --name "Farrukh Rahimov" --email "farrukh@example.tj" --phone "+992901234567"
echo ""
echo "Press Enter to continue..."
read

echo "=========================================="
echo "Test 3: Check same office (should show conflict)"
echo "Command: python3 main.py check-availability --office-id 1 --date 2025-12-05 --start-time 11:00 --end-time 13:00"
python3 main.py check-availability --office-id 1 --date 2025-12-05 --start-time 11:00 --end-time 13:00
echo ""
echo "Press Enter to continue..."
read

echo "=========================================="
echo "Test 4: Get office info (should show occupied)"
echo "Command: python3 main.py info --office-id 1 --date 2025-12-05 --start-time 11:00 --end-time 11:30"
python3 main.py info --office-id 1 --date 2025-12-05 --start-time 11:00 --end-time 11:30
echo ""
echo "Press Enter to continue..."
read

echo "=========================================="
echo "Test 5: Try to book conflicting time (should fail)"
echo "Command: python3 main.py book --office-id 1 --date 2025-12-05 --start-time 11:00 --end-time 13:00 --name 'Shohruh Mahmudov' --email 'shohruh@example.tj' --phone '+992917654321'"
python3 main.py book --office-id 1 --date 2025-12-05 --start-time 11:00 --end-time 13:00 --name "Shohruh Mahmudov" --email "shohruh@example.tj" --phone "+992917654321"
echo ""
echo "Press Enter to continue..."
read

echo "=========================================="
echo "Test 6: Book different office (should succeed)"
echo "Command: python3 main.py book --office-id 2 --date 2025-12-05 --start-time 10:00 --end-time 12:00 --name 'Dilshod Alimov' --email 'dilshod@example.tj' --phone '+992935555555'"
python3 main.py book --office-id 2 --date 2025-12-05 --start-time 10:00 --end-time 12:00 --name "Dilshod Alimov" --email "dilshod@example.tj" --phone "+992935555555"
echo ""
echo "Press Enter to continue..."
read

echo "=========================================="
echo "Test 7: Book office 1 at different time (should succeed)"
echo "Command: python3 main.py book --office-id 1 --date 2025-12-05 --start-time 14:00 --end-time 16:00 --name 'Zarina Safarova' --email 'zarina@example.tj' --phone '+992948888888'"
python3 main.py book --office-id 1 --date 2025-12-05 --start-time 14:00 --end-time 16:00 --name "Zarina Safarova" --email "zarina@example.tj" --phone "+992948888888"
echo ""

echo "=========================================="
echo "All tests completed!"
echo "=========================================="
