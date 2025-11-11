"""
Tester l'API conversations pour voir le format exact des données
"""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

try:
    print("🔍 Test: Récupérer conversations avec format admin...\n")
    
    result = supabase.from_("conversations").select("""
        *,
        merchant:merchant_id(id, username, email, company_name),
        influencer:influencer_id(id, username, email)
    """).order("last_message_at", desc=True).limit(3).execute()
    
    if result.data:
        print(f"✅ {len(result.data)} conversations récupérées\n")
        
        for i, conv in enumerate(result.data, 1):
            print(f"{'='*60}")
            print(f"Conversation {i} - ID: {conv.get('id')}")
            print(f"{'='*60}")
            
            merchant = conv.get('merchant', {})
            influencer = conv.get('influencer', {})
            
            print(f"\n📦 MERCHANT:")
            print(f"   - ID: {merchant.get('id')}")
            print(f"   - Username: {merchant.get('username')}")
            print(f"   - Company: {merchant.get('company_name')}")
            print(f"   - Email: {merchant.get('email')}")
            
            print(f"\n👤 INFLUENCER:")
            print(f"   - ID: {influencer.get('id')}")
            print(f"   - Username: {influencer.get('username')}")
            print(f"   - Email: {influencer.get('email')}")
            
            print(f"\n💬 MESSAGE:")
            print(f"   - Dernier: {conv.get('last_message')[:60]}...")
            print(f"   - Date: {conv.get('last_message_at')}")
            print(f"   - Non lus (merchant): {conv.get('unread_count_merchant')}")
            print(f"   - Non lus (influencer): {conv.get('unread_count_influencer')}")
            print()
    else:
        print("⚠️ Aucune conversation trouvée")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
