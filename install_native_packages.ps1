# Packages à installer après les Build Tools C++

# Retourner dans le backend
Set-Location "C:\Users\samye\OneDrive\Desktop\version tres avancee\versionlivrable\backend"

# Installer les packages qui nécessitent une compilation
& "C:/Users/samye/OneDrive/Desktop/version tres avancee/versionlivrable/.venv/Scripts/python.exe" -m pip install gevent==24.11.1

# Installer aiohttp 
& "C:/Users/samye/OneDrive/Desktop/version tres avancee/versionlivrable/.venv/Scripts/python.exe" -m pip install aiohttp==3.12.14

# Installer jq si nécessaire
& "C:/Users/samye/OneDrive/Desktop/version tres avancee/versionlivrable/.venv/Scripts/python.exe" -m pip install jq==1.10.0

# Installer Pillow avec la bonne version
& "C:/Users/samye/OneDrive/Desktop/version tres avancee/versionlivrable/.venv/Scripts/python.exe" -m pip install Pillow==10.2.0

Write-Host "✅ Installation terminée avec les Build Tools C++"