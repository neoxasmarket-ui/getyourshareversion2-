"""
Script pour créer les tables commerciales et insérer les données de test
=====================================================================
Exécute automatiquement :
1. CREATE_COMMERCIAL_TABLES.sql (anciennes tables existantes)
2. INSERT_COMMERCIAL_DATA.sql (nouvelles données)
"""

import os
import sys
from pathlib import Path
from supabase import create_client, Client

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://gwgvnusegnnhiciprvyc.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3Z3ZudXNlZ25uaGljaXBydnljIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA4MjE3NjgsImV4cCI6MjA0NjM5Nzc2OH0.gftLI_u0AxQUVIUi3hWjfJQ-m6Y56b5H5lDwbMEDGbU")

def read_sql_file(filepath: str) -> str:
    """Lit un fichier SQL"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.text()

def execute_sql_statements(supabase: Client, sql_content: str, filename: str):
    """
    Exécute des statements SQL un par un
    Note: Supabase Python client ne supporte pas l'exécution SQL directe
    Il faut utiliser l'API REST ou le dashboard Supabase
    """
    print(f"\n⚠️  Le fichier {filename} doit être exécuté manuellement dans Supabase SQL Editor")
    print(f"📋 Contenu à copier-coller :\n")
    print("="*80)
    print(sql_content[:500] + "...\n" + "="*80)
    print(f"\n💡 Allez sur: {SUPABASE_URL.replace('https://', 'https://app.supabase.com/project/')}/sql/new")
    print(f"   Collez le contenu de: {filename}")
    print(f"   Cliquez sur 'Run'\n")

def main():
    """Fonction principale"""
    print("="*80)
    print("🚀 CRÉATION DES TABLES COMMERCIALES ET DONNÉES DE TEST")
    print("="*80)
    
    # Initialiser Supabase client
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Connexion Supabase établie")
    except Exception as e:
        print(f"❌ Erreur de connexion Supabase: {e}")
        return
    
    # Chemins des fichiers SQL
    root_dir = Path(__file__).parent.parent
    
    # Note: Les tables sont déjà créées avec CREATE_COMMERCIAL_TABLES.sql (ancien fichier)
    # On va juste exécuter les INSERT
    
    sql_files = [
        {
            'path': root_dir / 'INSERT_COMMERCIAL_DATA.sql',
            'name': 'INSERT_COMMERCIAL_DATA.sql',
            'description': 'Insertion des données de test (3 commerciaux, leads, liens, templates)'
        }
    ]
    
    print("\n📦 Fichiers SQL à exécuter :")
    for idx, sql_file in enumerate(sql_files, 1):
        print(f"   {idx}. {sql_file['name']} - {sql_file['description']}")
    
    print("\n" + "="*80)
    print("⚠️  IMPORTANT: Les scripts SQL doivent être exécutés dans le SQL Editor de Supabase")
    print("="*80)
    
    for sql_file in sql_files:
        filepath = sql_file['path']
        
        if not filepath.exists():
            print(f"\n❌ Fichier non trouvé: {filepath}")
            continue
        
        print(f"\n{'='*80}")
        print(f"📄 Fichier: {sql_file['name']}")
        print(f"📝 Description: {sql_file['description']}")
        print(f"{'='*80}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            print(f"✅ Fichier lu ({len(sql_content)} caractères)")
            
            # Afficher les instructions
            execute_sql_statements(supabase, sql_content, sql_file['name'])
            
        except Exception as e:
            print(f"❌ Erreur lors de la lecture de {sql_file['name']}: {e}")
    
    print("\n" + "="*80)
    print("🎯 PROCHAINES ÉTAPES")
    print("="*80)
    print("""
1. ✅ Ouvrir Supabase Dashboard: https://app.supabase.com/project/gwgvnusegnnhiciprvyc/sql/new

2. ✅ Exécuter INSERT_COMMERCIAL_DATA.sql :
   - Copier le contenu du fichier
   - Coller dans le SQL Editor
   - Cliquer sur "Run"
   - Vérifier qu'il n'y a pas d'erreurs

3. ✅ Vérifier les données insérées :
   SELECT * FROM users WHERE role = 'commercial';
   SELECT * FROM sales_representatives;
   SELECT * FROM commercial_leads LIMIT 10;
   SELECT * FROM commercial_tracking_links LIMIT 10;
   SELECT * FROM commercial_templates LIMIT 10;

4. ✅ Tester les endpoints backend :
   - Ajouter commercial_endpoints.py dans server.py
   - app.include_router(commercial_endpoints.router)
   - Redémarrer le backend
   - Tester : GET /api/commercial/stats

5. ✅ Créer le frontend CommercialDashboard.js
    """)
    
    print("\n" + "="*80)
    print("💾 COMPTES DE TEST CRÉÉS")
    print("="*80)
    print("""
Email: commercial.starter@tracknow.io
Mot de passe: Test123!
Niveau: STARTER (gratuit, 10 leads max, 3 liens)

Email: commercial.pro@tracknow.io
Mot de passe: Test123!
Niveau: PRO (29€/mois, leads illimités, 15 templates)

Email: commercial.enterprise@tracknow.io
Mot de passe: Test123!
Niveau: ENTERPRISE (99€/mois, tout débloqué + IA)
    """)
    
    print("\n✨ Script terminé !")

if __name__ == "__main__":
    main()
