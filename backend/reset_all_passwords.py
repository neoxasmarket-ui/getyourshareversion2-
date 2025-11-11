"""
Réinitialise TOUS les mots de passe à Test123!
"""
from supabase_client import supabase
from db_helpers import hash_password

# Nouveau mot de passe pour TOUS les comptes
NEW_PASSWORD = "Test123!"
hashed = hash_password(NEW_PASSWORD)

print("Mise à jour de TOUS les comptes avec le mot de passe: Test123!")
print("="*60)

# Récupérer tous les utilisateurs
result = supabase.table("users").select("id, email, role").execute()
users = result.data

count = 0
for user in users:
    try:
        supabase.table("users").update({
            "password_hash": hashed,
            "is_active": True,
            "status": "active"
        }).eq("id", user["id"]).execute()
        
        print(f"✅ {user['email']} ({user['role']})")
        count += 1
    except Exception as e:
        print(f"❌ {user['email']}: {e}")

print("="*60)
print(f"✅ {count} comptes mis à jour")
print(f"\n🔑 Mot de passe universel: {NEW_PASSWORD}")
print("\nVous pouvez maintenant vous connecter avec:")
print("  - N'importe quel email de la base")
print(f"  - Mot de passe: {NEW_PASSWORD}")
