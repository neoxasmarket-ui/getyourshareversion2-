import sys
import os

backend_path = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_path)
os.chdir(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv("backend/.env")

from utils.supabase_client import get_supabase_client

supabase = get_supabase_client()

print("\n🔧 Exécution du script SQL pour ajouter le rôle 'commercial'...\n")

try:
    # Lire le script SQL
    with open('ADD_COMMERCIAL_ROLE.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Extraire uniquement les commandes SQL (ignorer les commentaires)
    sql_commands = []
    for line in sql_content.split('\n'):
        line = line.strip()
        if line and not line.startswith('--'):
            sql_commands.append(line)
    
    # Commande 1: Supprimer l'ancienne contrainte
    print("1️⃣  Suppression de l'ancienne contrainte...")
    result1 = supabase.rpc('exec_sql', {
        'query': 'ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check'
    }).execute()
    print("   ✅ Ancienne contrainte supprimée\n")
    
    # Commande 2: Ajouter la nouvelle contrainte
    print("2️⃣  Ajout de la nouvelle contrainte avec le rôle 'commercial'...")
    result2 = supabase.rpc('exec_sql', {
        'query': "ALTER TABLE users ADD CONSTRAINT users_role_check CHECK (role IN ('admin', 'merchant', 'influencer', 'commercial', 'affiliate'))"
    }).execute()
    print("   ✅ Nouvelle contrainte ajoutée\n")
    
    print("✅ Script SQL exécuté avec succès!")
    print("\n🎉 Le rôle 'commercial' est maintenant disponible!\n")
    
except Exception as e:
    error_msg = str(e)
    
    if "function public.exec_sql" in error_msg or "does not exist" in error_msg:
        print("⚠️  La fonction exec_sql n'existe pas dans Supabase.")
        print("\n📋 Vous devez exécuter le script SQL manuellement:\n")
        print("1. Ouvrez: https://supabase.com/dashboard")
        print("2. Allez dans: SQL Editor > New Query")
        print("3. Copiez-collez ces 2 lignes:\n")
        print("   ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check;")
        print("   ALTER TABLE users ADD CONSTRAINT users_role_check CHECK (role IN ('admin', 'merchant', 'influencer', 'commercial', 'affiliate'));\n")
        print("4. Cliquez sur 'Run'\n")
        print("💡 Ou dites-moi que vous l'avez fait, et je créerai les commerciaux!")
    else:
        print(f"❌ Erreur: {error_msg}")
        print("\n📋 Veuillez exécuter le script SQL manuellement dans Supabase.")
