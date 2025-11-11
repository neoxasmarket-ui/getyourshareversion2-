"""Vérifier les plans d'abonnement des comptes de test"""
from supabase_client import supabase

comptes_test = [
    # Influenceurs
    "hassan.oudrhiri@getyourshare.com",
    "sarah.benali@getyourshare.com", 
    "karim.benjelloun@getyourshare.com",
    # Marchands
    "boutique.maroc@getyourshare.com",
    "luxury.crafts@getyourshare.com",
    "electromaroc@getyourshare.com",
    # Commercial
    "sofia.chakir@getyourshare.com"
]

print("\n" + "="*70)
print("VÉRIFICATION DES PLANS D'ABONNEMENT")
print("="*70 + "\n")

for email in comptes_test:
    result = supabase.table("users").select("email, role, subscription_plan").eq("email", email).execute()
    
    if result.data:
        user = result.data[0]
        plan = user.get("subscription_plan", "N/A")
        role = user.get("role", "N/A")
        print(f"✅ {email}")
        print(f"   Rôle: {role}")
        print(f"   Plan: {plan}")
        print()
    else:
        print(f"❌ {email} - NON TROUVÉ")
        print()
