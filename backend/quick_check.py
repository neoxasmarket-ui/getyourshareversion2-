"""Quick check des utilisateurs"""
from supabase_client import supabase

try:
    result = supabase.table("users").select("email, role, password_hash").limit(5).execute()
    print("\n=== PREMIERS UTILISATEURS ===")
    for user in result.data:
        has_hash = "OUI" if user.get("password_hash") else "NON"
        print(f"{user['email']} ({user['role']}) - Hash: {has_hash}")
except Exception as e:
    print(f"Erreur: {e}")
