@echo off
echo ========================================
echo   ShareYourSales - Demarrage Complet
echo ========================================
echo.
echo Demarrage de tous les serveurs...
echo.

REM Démarrer Backend dans une nouvelle fenêtre
start "Backend - FastAPI" cmd /k "cd backend && C:\Users\samye\OneDrive\Desktop\v3\getyourshareversion2-\.venv\Scripts\python.exe -m uvicorn server:app --reload --host 0.0.0.0 --port 8000"

REM Attendre 5 secondes
timeout /t 5 /nobreak > nul

REM Démarrer Frontend dans une nouvelle fenêtre
start "Frontend - React" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo   Serveurs demarres !
echo ========================================
echo.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo   Docs API: http://localhost:8000/docs
echo.
echo Appuyez sur une touche pour arreter tous les serveurs...
pause > nul

REM Fermer toutes les fenêtres
taskkill /FI "WindowTitle eq Backend - FastAPI*" /F
taskkill /FI "WindowTitle eq Frontend - React*" /F
