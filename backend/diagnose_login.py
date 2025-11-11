"""
Script de diagnostic pour identifier les problèmes de connexion
"""
from supabase_client import supabase
from db_helpers import verify_password, hash_password
import sys

def check_users():
    """Vérifie tous les utilisateurs dans la base de données"""
    print("=" * 80)
    print("DIAGNOSTIC DES COMPTES UTILISATEURS")
    print("=" * 80)
    
    # Récupérer tous les utilisateurs
    result = supabase.table("users").select("id, email, role, password_hash, is_active, status").execute()
    users = result.data if result.data else []
    
    if not users:
        print("❌ AUCUN UTILISATEUR TROUVÉ DANS LA BASE DE DONNÉES")
        return
    
    print(f"\n✅ {len(users)} utilisateurs trouvés\n")
    
    problem_count = 0
    
    for user in users:
        email = user.get("email", "N/A")
        role = user.get("role", "N/A")
        password_hash = user.get("password_hash")
        is_active = user.get("is_active", True)
        status = user.get("status", "active")
        
        print(f"\n{'='*60}")
        print(f"📧 Email: {email}")
        print(f"👤 Rôle: {role}")
        print(f"🔒 Password hash présent: {'✅ OUI' if password_hash else '❌ NON'}")
        print(f"✔️  Actif: {'✅ OUI' if is_active else '❌ NON'}")
        print(f"📊 Status: {status}")
        
        # Vérifier si le password_hash est valide
        if password_hash:
            # Vérifier le format bcrypt (doit commencer par $2b$ ou $2a$ ou $2y$)
            if password_hash.startswith('$2'):
                print(f"🔐 Format hash: ✅ VALIDE (bcrypt)")
            else:
                print(f"🔐 Format hash: ❌ INVALIDE (pas bcrypt)")
                problem_count += 1
        else:
            print(f"⚠️  PROBLÈME: Pas de hash de mot de passe!")
            problem_count += 1
        
        # Vérifier si le compte peut se connecter
        if not is_active or status not in ['active', 'pending']:
            print(f"⚠️  PROBLÈME: Compte inactif ou status invalide")
            problem_count += 1
    
    print(f"\n{'='*80}")
    if problem_count == 0:
        print("✅ TOUS LES COMPTES SONT OK")
    else:
        print(f"❌ {problem_count} PROBLÈME(S) DÉTECTÉ(S)")
    print("=" * 80)

def test_login(email: str, password: str):
    """Teste la connexion avec un email et mot de passe"""
    print(f"\n\n{'='*80}")
    print(f"TEST DE CONNEXION: {email}")
    print("=" * 80)
    
    # Récupérer l'utilisateur
    result = supabase.table("users").select("*").eq("email", email).execute()
    
    if not result.data:
        print(f"❌ Utilisateur non trouvé: {email}")
        return False
    
    user = result.data[0]
    print(f"✅ Utilisateur trouvé")
    print(f"   Rôle: {user.get('role')}")
    print(f"   Actif: {user.get('is_active', True)}")
    print(f"   Status: {user.get('status', 'N/A')}")
    
    # Vérifier le mot de passe
    password_hash = user.get("password_hash")
    if not password_hash:
        print("❌ Pas de hash de mot de passe dans la base!")
        return False
    
    print(f"✅ Hash présent dans la base")
    
    # Tester la vérification
    try:
        is_valid = verify_password(password, password_hash)
        if is_valid:
            print(f"✅ MOT DE PASSE VALIDE - LA CONNEXION DEVRAIT FONCTIONNER")
            return True
        else:
            print(f"❌ MOT DE PASSE INVALIDE")
            return False
    except Exception as e:
        print(f"❌ ERREUR lors de la vérification: {e}")
        return False

if __name__ == "__main__":
    # Diagnostic complet
    check_users()
    
    # Tests de connexion avec les comptes connus
    print("\n\n" + "="*80)
    print("TESTS DE CONNEXION AVEC LES COMPTES COMMERCIAUX")
    print("="*80)
    
    test_accounts = [
        ("admin@getyourshare.com", "Admin123!"),
        ("commercial.free@getyourshare.com", "Test123!"),
        ("commercial.starter@getyourshare.com", "Test123!"),
    ]
    
    for email, password in test_accounts:
        test_login(email, password)
