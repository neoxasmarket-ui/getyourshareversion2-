"""
Test pour vérifier les conversations
"""

from supabase_client import supabase

try:
    # Test 1: Compter les conversations
    print("📊 Test 1: Vérifier les conversations...")
    result = supabase.from_("conversations").select("*", count="exact").execute()
    print(f"✅ {result.count} conversations trouvées")
    
    if result.data:
        conv = result.data[0]
        print(f"   Première conversation ID: {conv.get('id')}")
        print(f"   Merchant ID: {conv.get('merchant_id')}")
        print(f"   Influencer ID: {conv.get('influencer_id')}")
        print(f"   Last message: {conv.get('last_message')}")
    
    # Test 2: Compter les messages
    print("\n📊 Test 2: Vérifier les messages...")
    result = supabase.from_("messages").select("*", count="exact").execute()
    print(f"✅ {result.count} messages trouvés")
    
    # Test 3: Test avec JOIN
    print("\n📊 Test 3: Test avec JOIN users...")
    result = supabase.from_("conversations").select("""
        *,
        merchant:merchant_id(id, email, company_name),
        influencer:influencer_id(id, email, username)
    """).limit(3).execute()
    
    print(f"✅ {len(result.data)} conversations avec détails")
    if result.data:
        for conv in result.data:
            merchant = conv.get('merchant', {})
            influencer = conv.get('influencer', {})
            print(f"   - {merchant.get('company_name', 'N/A')} ↔ {influencer.get('username', 'N/A')}")
    
    print("\n✨ Tous les tests réussis !")
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
