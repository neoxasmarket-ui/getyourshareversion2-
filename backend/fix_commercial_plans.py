"""Vérifier et corriger les plans des commerciaux"""
from supabase_client import supabase

# Plans des commerciaux selon leurs emails
commerciaux = {
    "commercial.free@getyourshare.com": "free",
    "commercial.starter@getyourshare.com": "starter",
    "commercial.pro@getyourshare.com": "professional",
    "commercial.premium@getyourshare.com": "premium",
    "fatima.bennani@getyourshare.com": "starter",
    "youssef.alami@getyourshare.com": "professional"
}

print("\n" + "="*70)
print("CORRECTION DES PLANS DES COMMERCIAUX")
print("="*70 + "\n")

for email, expected_plan in commerciaux.items():
    # Vérifier le plan actuel
    result = supabase.table("users").select("subscription_plan").eq("email", email).execute()
    
    if result.data:
        current_plan = result.data[0].get("subscription_plan")
        
        if current_plan != expected_plan:
            # Corriger
            supabase.table("users").update({"subscription_plan": expected_plan}).eq("email", email).execute()
            print(f"✅ {email:45} {current_plan} → {expected_plan}")
        else:
            print(f"✓  {email:45} {expected_plan} (OK)")
    else:
        print(f"❌ {email:45} NON TROUVÉ")

print("\n" + "="*70)
print("✅ Vérification terminée")
print("="*70 + "\n")
