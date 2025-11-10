#!/bin/bash

# Script d'installation COMPLÈTE des dépendances backend
# Résout TOUS les problèmes de dépendances

set -e

echo "🔧 Installation des dépendances critiques Python..."

# Dépendances système critiques
apt-get update -qq
apt-get install -y -qq build-essential python3-dev libffi-dev libssl-dev 2>/dev/null || true

# Installer pip et upgrade
python3 -m pip install --upgrade pip setuptools wheel --quiet

# Nettoyer les installations cassées
pip uninstall -y pydantic pydantic-core fastapi 2>/dev/null || true

# Installer les dépendances DANS LE BON ORDRE
echo "📦 Installation packages de base..."
pip install --no-cache-dir \
    "pydantic-core==2.41.5" \
    "pydantic==2.12.3" \
    "fastapi==0.109.1" \
    "uvicorn[standard]==0.24.0" \
    "email-validator==2.3.0" \
    --quiet

echo "📦 Installation crypto & auth..."
pip install --no-cache-dir \
    bcrypt==4.1.3 \
    passlib==1.7.4 \
    "PyJWT==2.10.1" \
    python-jose==3.4.0 \
    python-multipart==0.0.18 \
    cryptography==46.0.3 \
    --quiet

echo "📦 Installation database & storage..."
pip install --no-cache-dir \
    supabase==2.22.1 \
    python-dotenv==1.1.1 \
    --quiet

echo "📦 Installation scheduling & tasks..."
pip install --no-cache-dir \
    APScheduler==3.10.4 \
    celery==5.3.6 \
    redis==5.0.1 \
    --quiet

echo "📦 Installation monitoring & logging..."
pip install --no-cache-dir \
    structlog==23.3.0 \
    sentry-sdk==1.40.0 \
    psutil==5.9.8 \
    --quiet

echo "📦 Installation payment & services..."
pip install --no-cache-dir \
    stripe==11.2.0 \
    pyotp==2.9.0 \
    qrcode==7.4.2 \
    --quiet

echo "📦 Installation server production..."
pip install --no-cache-dir \
    gunicorn==23.0.0 \
    gevent==24.11.1 \
    slowapi==0.1.9 \
    --quiet

echo "✅ TOUTES les dépendances sont installées!"
echo ""
echo "📋 Versions installées:"
python3 -c "import fastapi, pydantic, uvicorn, supabase, bcrypt; print(f'FastAPI: {fastapi.__version__}'); print(f'Pydantic: {pydantic.__version__}'); print(f'Uvicorn: {uvicorn.__version__}')"
echo ""
