#!/bin/bash

# ============================================
# Script de lancement GetYourShare
# Lance le backend et le frontend en mode développement
# ============================================

set -e

echo "🚀 Démarrage de GetYourShare..."
echo ""

# Couleurs pour les logs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vérifier si nous sommes dans le bon répertoire
if [ ! -f "package.json" ] && [ ! -d "backend" ] && [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Erreur: Ce script doit être exécuté depuis la racine du projet${NC}"
    exit 1
fi

# Fonction pour nettoyer les processus en arrière-plan
cleanup() {
    echo -e "\n${YELLOW}⏸️  Arrêt des services...${NC}"
    jobs -p | xargs -r kill 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# ============================================
# 1. VÉRIFICATION DES PRÉREQUIS
# ============================================

echo -e "${BLUE}📋 Vérification des prérequis...${NC}"

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $(python3 --version | cut -d' ' -f2)${NC}"

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js n'est pas installé${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js $(node --version)${NC}"

# Vérifier npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm n'est pas installé${NC}"
    exit 1
fi
echo -e "${GREEN}✅ npm $(npm --version)${NC}"

echo ""

# ============================================
# 2. INSTALLATION DES DÉPENDANCES BACKEND
# ============================================

echo -e "${BLUE}📦 Installation des dépendances backend...${NC}"
cd backend

# Vérifier si les dépendances sont installées
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Environnement virtuel non trouvé, création...${NC}"
    python3 -m venv venv
fi

# Activer l'environnement virtuel
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Installer les dépendances
pip install -q -r requirements.txt

echo -e "${GREEN}✅ Dépendances backend installées${NC}"

cd ..

# ============================================
# 3. INSTALLATION DES DÉPENDANCES FRONTEND
# ============================================

echo -e "${BLUE}📦 Installation des dépendances frontend...${NC}"
cd frontend

# Installer les dépendances si nécessaire
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules non trouvé, installation...${NC}"
    npm install
else
    echo -e "${GREEN}✅ node_modules déjà installé${NC}"
fi

cd ..

echo ""

# ============================================
# 4. VÉRIFICATION DES VARIABLES D'ENVIRONNEMENT
# ============================================

echo -e "${BLUE}🔧 Vérification de la configuration...${NC}"

if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠️  Fichier backend/.env non trouvé${NC}"
    echo -e "${YELLOW}   Copie depuis .env.example...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✅ Fichier .env créé. Veuillez le configurer avec vos clés API${NC}"
fi

if [ ! -f "frontend/.env" ]; then
    if [ -f "frontend/.env.example" ]; then
        echo -e "${YELLOW}⚠️  Fichier frontend/.env non trouvé${NC}"
        echo -e "${YELLOW}   Copie depuis .env.example...${NC}"
        cp frontend/.env.example frontend/.env
    fi
fi

echo ""

# ============================================
# 5. LANCEMENT DES SERVICES
# ============================================

echo -e "${GREEN}🎯 Lancement des services...${NC}"
echo ""

# Lancer le backend
echo -e "${BLUE}🔷 Démarrage du backend (port 8000)...${NC}"
cd backend
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Utiliser server.py par défaut (version Supabase)
python3 -m uvicorn server:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Attendre que le backend démarre
echo -e "${YELLOW}⏳ Attente du démarrage du backend...${NC}"
sleep 3

# Lancer le frontend
echo -e "${BLUE}🔷 Démarrage du frontend (port 3000)...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ GetYourShare est lancé avec succès!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📍 URLs:${NC}"
echo -e "   🌐 Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "   🔧 Backend API: ${GREEN}http://localhost:8000${NC}"
echo -e "   📚 Documentation API: ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}💡 Pour arrêter les services: Ctrl+C${NC}"
echo ""

# Garder le script actif et attendre les processus
wait
