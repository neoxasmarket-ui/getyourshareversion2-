"""Mettre à jour les plans d'abonnement selon les boutons de connexion rapide"""
from supabase_client import supabase

# Mapping des comptes avec leurs vrais plans
comptes_plans = {
    # Influenceurs
    "hassan.oudrhiri@getyourshare.com": "starter",
    "sarah.benali@getyourshare.com": "professional",
    "karim.benjelloun@getyourshare.com": "premium",
    
    # Marchands
    "boutique.maroc@getyourshare.com": "starter",
    "luxury.crafts@getyourshare.com": "professional",
    "electromaroc@getyourshare.com": "premium",
    
    # Admin reste admin
    "admin@getyourshare.com": "premium",
    "sofia.chakir@getyourshare.com": "premium"
}

print("\n" + "="*70)
print("MISE À JOUR DES PLANS D'ABONNEMENT")
print("="*70 + "\n")

for email, plan in comptes_plans.items():
    try:
        # Mettre à jour le plan
        result = supabase.table("users").update({
            "subscription_plan": plan
        }).eq("email", email).execute()
        
        if result.data:
            print(f"✅ {email:45} → {plan.upper()}")
        else:
            print(f"⚠️  {email:45} → Compte non trouvé")
    except Exception as e:
        print(f"❌ {email:45} → Erreur: {e}")

print("\n" + "="*70)
print("✅ Mise à jour terminée")
print("="*70)
print("\nLes boutons de connexion rapide correspondent maintenant aux vrais plans!\n")
