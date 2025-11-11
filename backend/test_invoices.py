"""
Test rapide pour vérifier si les factures sont accessibles
"""

from supabase_client import supabase

try:
    # Test 1: Query simple sans JOIN
    print("📊 Test 1: Query simple des factures...")
    result = supabase.from_("invoices").select("*").limit(5).execute()
    print(f"✅ {len(result.data)} factures trouvées")
    if result.data:
        print(f"   Première facture: {result.data[0].get('invoice_number')}")
    
    # Test 2: Query avec JOIN
    print("\n📊 Test 2: Query avec JOIN users...")
    result = supabase.from_("invoices").select("""
        *,
        users!invoices_merchant_id_fkey(id, email, company_name)
    """).limit(5).execute()
    print(f"✅ {len(result.data)} factures avec merchants")
    if result.data:
        inv = result.data[0]
        print(f"   Facture: {inv.get('invoice_number')}")
        print(f"   Merchant: {inv.get('users', {}).get('company_name', 'N/A')}")
    
    # Test 3: Count total
    print("\n📊 Test 3: Count total...")
    result = supabase.from_("invoices").select("*", count="exact").execute()
    print(f"✅ Total: {result.count} factures")
    
    print("\n✨ Tous les tests réussis !")
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
