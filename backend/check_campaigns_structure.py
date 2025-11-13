"""
Vérifier la structure de la table campaigns
"""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

print("\n🔍 Vérification structure table 'campaigns'...\n")

try:
    # Essayer de récupérer une campagne vide pour voir la structure
    response = supabase.table("campaigns").select("*").limit(1).execute()
    
    if response.data:
        print("✅ Table 'campaigns' existe avec données:")
        print(f"   Colonnes trouvées: {list(response.data[0].keys())}")
        print(f"\n📄 Exemple de donnée:")
        for key, value in response.data[0].items():
            print(f"   {key}: {value}")
    else:
        print("✅ Table 'campaigns' existe mais est vide")
        print("   Impossible de déterminer la structure exacte")
        
        # Essayer d'insérer une campagne minimale pour voir quelles colonnes sont requises
        print("\n🧪 Test d'insertion minimale...")
        
except Exception as e:
    print(f"❌ Erreur: {e}")
    print("\n💡 La table 'campaigns' n'existe probablement pas dans Supabase")
    print("   Vous devez d'abord exécuter le script SQL de création:")
    print("   backend/database/INIT_SUPABASE_COMPLET.sql")
