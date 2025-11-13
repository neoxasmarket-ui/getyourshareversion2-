"""
Script pour créer des demandes d'inscription d'annonceurs en attente
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Variables d'environnement SUPABASE manquantes!")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Demandes d'inscription en attente
pending_advertisers = [
    {
        "email": "fashion.pending@example.com",
        "username": "fashion_pending_001",
        "company_name": "Fashion Boutique Paris",
        "role": "merchant",
        "status": "pending",
        "country": "France",
        "phone": "+33612345678",
        "password_hash": "$2b$12$dummy_hash_for_testing"
    },
    {
        "email": "tech.pending@example.com",
        "username": "tech_pending_002",
        "company_name": "Tech Solutions Inc",
        "role": "merchant",
        "status": "pending",
        "country": "USA",
        "phone": "+1234567890",
        "password_hash": "$2b$12$dummy_hash_for_testing"
    },
    {
        "email": "beaute.pending@example.com",
        "username": "beaute_pending_003",
        "company_name": "Beauté Maroc",
        "role": "merchant",
        "status": "pending",
        "country": "Maroc",
        "phone": "+212612345678",
        "password_hash": "$2b$12$dummy_hash_for_testing"
    },
    {
        "email": "sports.pending@example.com",
        "username": "sports_pending_004",
        "company_name": "Sports Wear Shop",
        "role": "merchant",
        "status": "pending",
        "country": "France",
        "phone": "+33687654321",
        "password_hash": "$2b$12$dummy_hash_for_testing"
    },
    {
        "email": "gadgets.pending@example.com",
        "username": "gadgets_pending_005",
        "company_name": "Gadgets & Electronics",
        "role": "merchant",
        "status": "pending",
        "country": "Canada",
        "phone": "+1987654321",
        "password_hash": "$2b$12$dummy_hash_for_testing"
    }
]

print("\n" + "="*60)
print("🔄 CRÉATION DES DEMANDES D'INSCRIPTION EN ATTENTE")
print("="*60 + "\n")

try:
    # Vérifier si des utilisateurs existent déjà avec ces emails
    existing_emails = []
    for advertiser in pending_advertisers:
        result = supabase.from_("users").select("email").eq("email", advertiser["email"]).execute()
        if result.data:
            existing_emails.append(advertiser["email"])
    
    if existing_emails:
        print("⚠️  Les emails suivants existent déjà:")
        for email in existing_emails:
            print(f"   - {email}")
        print("\n🗑️  Suppression des doublons...")
        
        for email in existing_emails:
            supabase.from_("users").delete().eq("email", email).execute()
        print("✅ Doublons supprimés\n")
    
    # Insérer les nouvelles demandes
    print("📝 Insertion des demandes d'inscription...")
    result = supabase.from_("users").insert(pending_advertisers).execute()
    
    print(f"✅ {len(pending_advertisers)} demandes d'inscription créées!\n")
    
    print("📊 RÉSUMÉ DES DEMANDES CRÉÉES:")
    print("-" * 60)
    for adv in pending_advertisers:
        print(f"   ✓ {adv['company_name']}")
        print(f"     Email: {adv['email']}")
        print(f"     Pays: {adv['country']}")
        print(f"     Statut: {adv['status']}")
        print()
    
    print("="*60)
    print("✅ CRÉATION TERMINÉE AVEC SUCCÈS!")
    print("="*60)
    print("\n🌐 Accédez à la page:")
    print("   http://localhost:3000/admin/advertiser-registrations")
    print("\n📝 Vous devriez maintenant voir 5 demandes en attente!\n")
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}\n")
    import traceback
    traceback.print_exc()
