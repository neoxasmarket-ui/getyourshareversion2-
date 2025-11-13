"""
============================================
SCRIPT D'EXÉCUTION DU SQL DE MODÉRATION
Crée les tables moderation_queue, moderation_history, etc.
============================================
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ Erreur: Variables d'environnement Supabase manquantes")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Lire le fichier SQL
sql_file = "database/CREATE_MODERATION_TABLES.sql"

if not os.path.exists(sql_file):
    print(f"❌ Fichier {sql_file} non trouvé")
    exit(1)

print("\n" + "="*60)
print("📊 CRÉATION DES TABLES DE MODÉRATION")
print("="*60 + "\n")

with open(sql_file, 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Séparer en plusieurs commandes (éviter les erreurs de syntaxe)
sql_commands = sql_content.split(';')

executed = 0
errors = 0

for i, command in enumerate(sql_commands):
    command = command.strip()
    if not command or command.startswith('--') or command.startswith('/*'):
        continue
    
    try:
        # Exécuter via RPC raw_sql si disponible, sinon via execute
        print(f"Exécution commande {i+1}... ", end='')
        
        # Note: Supabase Python client ne supporte pas l'exécution SQL directe
        # Il faut utiliser l'API REST ou créer une fonction SQL
        print("⚠️ Veuillez exécuter le SQL manuellement dans Supabase Dashboard")
        break
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        errors += 1

print("\n" + "="*60)
print("ℹ️ INSTRUCTIONS MANUELLES")
print("="*60)
print("""
1. Ouvrez Supabase Dashboard: https://supabase.com/dashboard
2. Allez dans votre projet
3. SQL Editor (menu gauche)
4. Copiez le contenu de: backend/database/CREATE_MODERATION_TABLES.sql
5. Collez dans l'éditeur SQL
6. Cliquez sur 'Run' ou Ctrl+Enter
7. Vérifiez que les tables sont créées (Table Editor)
8. Relancez ce script pour créer les données de test

📋 Tables à créer:
   - moderation_queue
   - moderation_history
   - moderation_stats
   - v_pending_moderation (vue)
   - v_daily_moderation_stats (vue)
""")
print("="*60 + "\n")
