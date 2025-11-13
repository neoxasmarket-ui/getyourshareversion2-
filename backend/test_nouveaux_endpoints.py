"""
TEST RAPIDE - Vérifier que tous les nouveaux endpoints sont accessibles
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Teste tous les nouveaux endpoints"""
    
    print("🧪 TEST DES NOUVEAUX ENDPOINTS")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1️⃣ Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2: Gamification endpoints
    print("\n2️⃣ Gamification - Badges...")
    try:
        response = requests.get(f"{BASE_URL}/api/gamification/badges")
        data = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Total badges: {data.get('total', 0)}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n3️⃣ Gamification - Missions...")
    try:
        response = requests.get(f"{BASE_URL}/api/gamification/missions")
        data = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Total missions: {data.get('total', 0)}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n4️⃣ Gamification - Leaderboard...")
    try:
        response = requests.get(f"{BASE_URL}/api/gamification/leaderboard?limit=5")
        data = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Total utilisateurs: {data.get('total', 0)}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Transaction endpoints
    print("\n5️⃣ Transactions - Pending...")
    try:
        response = requests.get(f"{BASE_URL}/api/transactions/pending")
        data = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Transactions en attente: {data.get('count', 0)}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 4: Webhook endpoints
    print("\n6️⃣ Webhooks - Stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/webhooks/stats?period=30d")
        data = response.json()
        print(f"   ✅ Status: {response.status_code}")
        stats = data.get('stats', {})
        print(f"   Total webhooks: {stats.get('total_webhooks', 0)}")
        print(f"   Taux de succès: {stats.get('success_rate', 0)}%")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n7️⃣ Webhooks - Logs...")
    try:
        response = requests.get(f"{BASE_URL}/api/webhooks/logs?limit=5")
        data = response.json()
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Total logs: {data.get('total', 0)}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 5: Test webhook POST
    print("\n8️⃣ Webhooks - Test POST...")
    try:
        payload = {
            "event_type": "test.manual",
            "source": "test_script",
            "payload": {
                "test": True,
                "message": "Test depuis script Python"
            }
        }
        response = requests.post(f"{BASE_URL}/api/webhooks/test", json=payload)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 6: Documentation
    print("\n9️⃣ Documentation OpenAPI...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"   ✅ Status: {response.status_code}")
        print(f"   Documentation accessible à: {BASE_URL}/docs")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS !")
    print("\n📚 Documentation complète:")
    print(f"   - Swagger UI: {BASE_URL}/docs")
    print(f"   - ReDoc: {BASE_URL}/redoc")
    print(f"   - OpenAPI JSON: {BASE_URL}/openapi.json")
    print("\n💡 Pour tester avec authentification, obtenez d'abord un token:")
    print(f"   curl -X POST {BASE_URL}/api/auth/login \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"email":"admin@getyourshare.com","password":"Admin123!"}\'')


if __name__ == "__main__":
    print("⏳ Assurez-vous que le serveur FastAPI tourne (python server.py)...")
    input("Appuyez sur Entrée pour commencer les tests...")
    test_endpoints()
