# Script de démarrage du serveur backend
# Utilisation: .\start_server.ps1

Write-Host ""
Write-Host "Demarrage du serveur FastAPI..." -ForegroundColor Cyan
Write-Host ""

# Chemins absolus
$projectRoot = "C:\Users\samye\OneDrive\Desktop\v3\getyourshareversion2-"
$backendPath = Join-Path $projectRoot "backend"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"

# Vérification
if (-not (Test-Path $pythonExe)) {
    Write-Host "❌ Python introuvable: $pythonExe" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $backendPath)) {
    Write-Host "❌ Dossier backend introuvable: $backendPath" -ForegroundColor Red
    exit 1
}

# Arrêt des processus existants
Write-Host "Arret des serveurs existants..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*uvicorn*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Navigation vers backend
Set-Location $backendPath
Write-Host "Repertoire: $backendPath" -ForegroundColor Gray
Write-Host ""

# Démarrage du serveur
Write-Host "Demarrage sur http://0.0.0.0:8000" -ForegroundColor Green
Write-Host ""
& $pythonExe -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
