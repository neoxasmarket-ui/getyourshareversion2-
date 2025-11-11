"""
Nettoyage complet de toutes les données mockées
ATTENTION: Ce script va SUPPRIMER des données !
"""
from supabase_client import supabase

print("\n" + "="*80)
print("🧹 NETTOYAGE DES DONNÉES MOCKÉES")
print("="*80)
print("\n⚠️  ATTENTION: Ce script va supprimer des données !")
print("   Appuyez sur Ctrl+C maintenant pour annuler\n")

input("Appuyez sur ENTER pour continuer...")

deleted_count = {}

# Liste des tables à nettoyer (avec condition)
tables_to_clean = [
    ("sales", "Ventes"),
    ("click_tracking", "Clics"),
    ("commissions", "Commissions"),
    ("affiliate_requests", "Demandes d'affiliation"),
    ("campaigns", "Campagnes"),
    ("products", "Produits"),
    ("services", "Services"),
]

print("\n" + "="*80)
print("SUPPRESSION EN COURS...")
print("="*80 + "\n")

for table_name, description in tables_to_clean:
    try:
        # Compter d'abord
        count_before = supabase.table(table_name).select("id", count="exact").execute().count or 0
        
        if count_before > 0:
            # Supprimer
            supabase.table(table_name).delete().neq("id", "").execute()
            
            # Vérifier
            count_after = supabase.table(table_name).select("id", count="exact").execute().count or 0
            deleted = count_before - count_after
            
            deleted_count[table_name] = deleted
            print(f"✅ {description:30} - {deleted} enregistrements supprimés")
        else:
            print(f"ℹ️  {description:30} - Déjà vide")
            
    except Exception as e:
        print(f"❌ {description:30} - Erreur: {e}")

print("\n" + "="*80)
print("RÉSUMÉ")
print("="*80)
total = sum(deleted_count.values())
print(f"\n✅ {total} enregistrements supprimés au total")
print("\n⚠️  Note: Les utilisateurs ont été conservés")
print("   Utilisez reset_all_passwords.py pour les mots de passe\n")
