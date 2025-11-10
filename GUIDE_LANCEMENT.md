# 🚀 Guide de Lancement GetYourShare

Guide rapide pour démarrer le projet en local après les corrections de stabilité.

## ✅ Corrections Appliquées

### Frontend
- ✅ Création du fichier manquant `frontend/src/utils/logger.js`
- ✅ Correction des chemins d'import dans `i18n/i18n.js`, `hooks/useLocalStorage.js` et `hooks/useWebSocket.js`
- ✅ Installation des dépendances manquantes:
  - `@tanstack/react-query@^5.0.0`
  - `@tanstack/react-query-devtools@^5.0.0`
  - `prop-types@^15.8.1`
- ✅ Résolution du doublon `OptimizedImage.jsx`

### Backend
- ✅ Correction des imports relatifs dans:
  - `tiktok_shop_endpoints.py`
  - `whatsapp_endpoints.py`
  - `content_studio_endpoints.py`

## 🎯 Méthode de Lancement Recommandée

### Option 1: Script Automatique (Recommandé)

```bash
# À la racine du projet
./start.sh
```

Le script va:
1. ✅ Vérifier les prérequis (Python, Node.js, npm)
2. 📦 Installer les dépendances backend
3. 📦 Installer les dépendances frontend
4. 🔧 Vérifier la configuration (.env)
5. 🚀 Lancer backend (port 8000)
6. 🚀 Lancer frontend (port 3000)

### Option 2: Lancement Manuel

#### Backend

```bash
cd backend

# Créer l'environnement virtuel (première fois)
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python3 -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Installer les dépendances (première fois)
npm install

# Lancer le serveur de développement
npm start
```

## 🌐 URLs d'Accès

Une fois lancé:
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **Documentation API**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc

## ⚙️ Configuration Requise

### Variables d'Environnement Backend

Fichier: `backend/.env`

```bash
# Supabase (REQUIS)
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_ANON_KEY=votre_cle_anon
SUPABASE_SERVICE_ROLE_KEY=votre_cle_service

# JWT (REQUIS)
JWT_SECRET=votre_secret_jwt_tres_long
JWT_ALGORITHM=HS256

# Application
ENVIRONMENT=development
PORT=8000

# Email (Resend)
RESEND_API_KEY=re_votre_cle
EMAIL_FROM_ADDRESS=onboarding@resend.dev

# Stripe (Optionnel en dev)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# OpenAI (Optionnel)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

### Variables d'Environnement Frontend

Fichier: `frontend/.env` (optionnel)

```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## 🔍 Vérification du Lancement

### Backend

Vérifier que le backend fonctionne:

```bash
curl http://localhost:8000/health
# Réponse attendue: {"status":"healthy"}
```

Ou ouvrir dans le navigateur:
- http://localhost:8000/docs (Swagger UI)

### Frontend

Ouvrir dans le navigateur:
- http://localhost:3000

La page d'accueil devrait se charger sans erreurs de console.

## 🐛 Résolution de Problèmes

### Erreur: "Module 'logger' not found" (Frontend)

**Solution**: Le fichier a été créé. Si l'erreur persiste:

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Erreur: "Cannot import name '...' from 'services...'" (Backend)

**Solution**: Les imports ont été corrigés. Si l'erreur persiste, vérifier que vous êtes dans le répertoire `backend/`:

```bash
cd backend
python3 -c "import sys; print(sys.path)"
```

### Erreur: "Package not found" (Frontend)

**Solution**: Les dépendances ont été installées. Réinstaller si nécessaire:

```bash
cd frontend
npm install @tanstack/react-query @tanstack/react-query-devtools prop-types
```

### Port déjà utilisé

Si le port 8000 ou 3000 est déjà utilisé:

**Backend** - Modifier le port:
```bash
uvicorn server:app --reload --port 8001
```

**Frontend** - Modifier dans `package.json`:
```json
"scripts": {
  "start": "PORT=3001 react-scripts start"
}
```

## 📦 Dépendances Installées

### Backend (Python)
- FastAPI 0.109.1
- Uvicorn 0.24.0
- Supabase 2.22.1
- Pydantic 2.12.3
- Python-dotenv 1.1.1
- + 100+ autres packages

### Frontend (React)
- React 18.2.0
- React Router DOM 6.20.0
- Material-UI 5.14.20
- Axios 1.6.2
- Framer Motion 12.23.24
- **@tanstack/react-query** 5.x (nouveau)
- **prop-types** 15.8.1 (nouveau)
- + autres dépendances

## 🎯 Structure du Projet

```
versionlivrable/
├── backend/                # API FastAPI + Supabase
│   ├── server.py          # Point d'entrée principal
│   ├── requirements.txt   # Dépendances Python
│   ├── .env              # Configuration
│   ├── services/         # Services métier
│   ├── routes/           # Routes API
│   └── ...
├── frontend/              # Application React
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── utils/        # ✅ logger.js ajouté ici
│   │   ├── hooks/
│   │   └── i18n/
│   ├── package.json
│   └── .env
├── start.sh              # ✅ Script de lancement automatique
└── GUIDE_LANCEMENT.md    # ✅ Ce fichier
```

## 🔒 Sécurité

⚠️ **Important**: Ne jamais commiter les fichiers `.env` avec des vraies clés API!

Les fichiers `.env` sont déjà dans `.gitignore`.

## 📚 Prochaines Étapes

1. ✅ Lancer le projet avec `./start.sh`
2. 🔑 Configurer les variables d'environnement dans `backend/.env`
3. 🗄️ Configurer Supabase (voir documentation)
4. 🧪 Tester les fonctionnalités principales
5. 📱 Tester l'interface utilisateur

## 🆘 Support

En cas de problème:

1. Vérifier les logs du backend et frontend
2. Vérifier la configuration `.env`
3. Consulter la documentation API: http://localhost:8000/docs
4. Vérifier les issues GitHub du projet

---

**Version**: 1.0.0
**Date**: 2025-11-10
**Status**: ✅ Stable - Prêt pour développement
