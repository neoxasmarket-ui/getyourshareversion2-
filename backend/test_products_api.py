"""
Test - Appeler l'API products directement
"""
import requests

# Test l'API sans authentification
try:
    response = requests.get("http://localhost:8000/api/products")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Total produits: {data.get('total', 0)}")
        
        if data.get('products'):
            print("\n📦 Premiers produits:")
            for i, p in enumerate(data['products'][:3], 1):
                print(f"{i}. {p.get('name')} - {p.get('price')}€")
    else:
        print(f"❌ Erreur: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Serveur non accessible sur http://localhost:8000")
except Exception as e:
    print(f"❌ Erreur: {e}")
