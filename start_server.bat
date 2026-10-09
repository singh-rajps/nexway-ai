@echo off
title Nexway Server
echo ===================================================
echo Starting Nexway IoT Device Management Server...
echo ===================================================

cd /d "D:\IOT DEVICE"

echo Opening browser...
start http://127.0.0.1:8000

echo Starting Python Backend Server...
uvicorn main:app --reload

pause
