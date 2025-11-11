@echo off
echo ========================================
echo   ShareYourSales - Backend Server
echo ========================================
echo.

cd backend
echo Demarrage du serveur FastAPI...
echo.

REM Démarrer le serveur avec le chemin absolu Python
C:\Users\samye\OneDrive\Desktop\v3\getyourshareversion2-\.venv\Scripts\python.exe -m uvicorn server:app --reload --host 0.0.0.0 --port 8000

pause
