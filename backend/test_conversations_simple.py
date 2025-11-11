"""
Test simple des conversations dans Supabase
"""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Service role pour bypass RLS

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    print("🔍 Test 1: Compter les conversations...")
    result = supabase.from_("conversations").select("*", count="exact").execute()
    print(f"✅ {result.count} conversations trouvées\n")
    
    print("🔍 Test 2: Compter les messages...")
    result = supabase.from_("messages").select("*", count="exact").execute()
    print(f"✅ {result.count} messages trouvés\n")
    
    print("🔍 Test 3: Détails des conversations...")
    result = supabase.from_("conversations").select("""
        *,
        merchant:merchant_id(id, email, company_name),
        influencer:influencer_id(id, email, username)
    """).limit(5).execute()
    
    if result.data:
        for i, conv in enumerate(result.data, 1):
            merchant = conv.get('merchant', {})
            influencer = conv.get('influencer', {})
            print(f"Conversation {i}:")
            print(f"  Marchand: {merchant.get('company_name', 'N/A')}")
            print(f"  Influenceur: {influencer.get('username', 'N/A')}")
            print(f"  Dernier message: {conv.get('last_message', '')[:60]}...")
            print(f"  Non lus (marchand): {conv.get('unread_count_merchant')}")
            print(f"  Non lus (influenceur): {conv.get('unread_count_influencer')}")
            print()
    else:
        print("⚠️ Aucune conversation avec détails\n")
    
    print("✅ Tests terminés!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
