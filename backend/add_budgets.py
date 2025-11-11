"""
Script pour ajouter des données budgétaires aux merchants
"""
import os
from supabase import create_client

# Charger manuellement les variables depuis .env
try:
    with open('.env', 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
except Exception as e:
    print(f"Erreur lors du chargement du .env: {e}")

# Connexion Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

print(f"URL: {supabase_url[:30] if supabase_url else 'None'}...")
print(f"Key: {'✅ Chargée' if supabase_key else '❌ Manquante'}\n")

supabase = create_client(supabase_url, supabase_key)

def add_budgets():
    """Ajoute des budgets réalistes aux merchants"""
    
    print("\n" + "="*60)
    print("🔧 AJOUT DES BUDGETS AUX MERCHANTS")
    print("="*60 + "\n")
    
    # Récupérer tous les merchants
    result = supabase.table("users").select("id, email, company_name").eq("role", "merchant").execute()
    merchants = result.data
    
    if not merchants:
        print("❌ Aucun merchant trouvé")
        return
    
    print(f"✅ {len(merchants)} merchants trouvés\n")
    
    # Données budgétaires réalistes
    budgets = [
        {"balance": 5000.00, "total_spent": 15000.00, "campaigns_count": 5, "country": "France", "company_name": "TechCorp SAS"},
        {"balance": 12500.50, "total_spent": 8700.25, "campaigns_count": 3, "country": "Maroc", "company_name": "Digital Marketing MA"},
        {"balance": 3200.00, "total_spent": 22000.00, "campaigns_count": 8, "country": "Belgique", "company_name": "E-Commerce Plus"},
        {"balance": 8750.75, "total_spent": 11200.50, "campaigns_count": 4, "country": "France", "company_name": "Innovation Labs"},
        {"balance": 15000.00, "total_spent": 5000.00, "campaigns_count": 2, "country": "Suisse", "company_name": "Swiss Retail AG"},
        {"balance": 2500.00, "total_spent": 18500.00, "campaigns_count": 6, "country": "Canada", "company_name": "Maple Marketing"},
        {"balance": 9800.00, "total_spent": 13400.00, "campaigns_count": 7, "country": "France", "company_name": "Paris Fashion"},
        {"balance": 20000.00, "total_spent": 3000.00, "campaigns_count": 1, "country": "Luxembourg", "company_name": "Finance First"},
    ]
    
    # Mettre à jour chaque merchant
    for i, merchant in enumerate(merchants):
        budget_data = budgets[i % len(budgets)]
        
        try:
            supabase.table("users").update({
                "balance": budget_data["balance"],
                "total_spent": budget_data["total_spent"],
                "campaigns_count": budget_data["campaigns_count"],
                "country": budget_data["country"],
                "company_name": budget_data["company_name"],
                "status": "active"
            }).eq("id", merchant["id"]).execute()
            
            print(f"✅ {merchant.get('email', 'N/A')}")
            print(f"   Entreprise: {budget_data['company_name']}")
            print(f"   Pays: {budget_data['country']}")
            print(f"   Balance: {budget_data['balance']} €")
            print(f"   Total dépensé: {budget_data['total_spent']} €")
            print(f"   Campagnes: {budget_data['campaigns_count']}")
            print()
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return
    
    print("\n" + "="*60)
    print("✅ BUDGETS AJOUTÉS AVEC SUCCÈS!")
    print("="*60)
    print("\n💡 Rafraîchissez la page 'Annonceurs'")

if __name__ == "__main__":
    add_budgets()
