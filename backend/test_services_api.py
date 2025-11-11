#!/usr/bin/env python3
"""
Test des endpoints /api/services
"""

import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db_helpers import get_all_services, get_service_by_id
from supabase import create_client
import json

# Initialiser Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://jmehgebizhfabgjgflkd.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImptZWhnZWJpemhmYWJnamdmbGtkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyMzU1ODUwOCwiZXhwIjoyMDM5MTM0NTA4fQ.pGIkBIw4qzaBT9d4BEVwdipKlLrjc52qsxmCPOCmBus")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🔍 TEST DES SERVICES")
print("=" * 60)

# Test 1: Récupérer tous les services
print("\n📋 Test 1: Récupération de tous les services")
print("-" * 60)
services = get_all_services()
print(f"✅ Total services: {len(services)}")

if services:
    print("\n🔹 Premier service:")
    first_service = services[0]
    print(f"   Nom: {first_service.get('name')}")
    print(f"   Catégorie: {first_service.get('category')}")
    print(f"   Prix par lead: {first_service.get('price_per_lead')}€")
    print(f"   Capacité/mois: {first_service.get('capacity_per_month')}")
    print(f"   Merchant ID: {first_service.get('merchant_id')}")
    
    if first_service.get('merchant'):
        print(f"   Merchant: {first_service['merchant'].get('company_name')}")
    
    if first_service.get('lead_requirements'):
        print(f"   Critères: {json.dumps(first_service['lead_requirements'], indent=6, ensure_ascii=False)}")

# Test 2: Récupérer par catégorie
print("\n📊 Test 2: Services par catégorie")
print("-" * 60)
categories = {}
for service in services:
    cat = service.get('category', 'Non défini')
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    print(f"   {cat}: {count} service(s)")

# Test 3: Récupérer un service spécifique
if services:
    print("\n🔍 Test 3: Récupération d'un service par ID")
    print("-" * 60)
    service_id = services[0].get('id')
    service = get_service_by_id(service_id)
    
    if service:
        print(f"✅ Service trouvé: {service.get('name')}")
        print(f"   ID: {service.get('id')}")
        print(f"   Description: {service.get('description')[:100]}...")
        print(f"   Tags: {service.get('tags')}")
    else:
        print("❌ Service non trouvé")

# Test 4: Vérifier les colonnes importantes
print("\n✅ Test 4: Vérification des colonnes")
print("-" * 60)
required_columns = [
    'id', 'merchant_id', 'name', 'description', 'category',
    'price_per_lead', 'capacity_per_month', 'lead_requirements',
    'tags', 'images', 'is_available', 'created_at'
]

if services:
    missing_columns = [col for col in required_columns if col not in services[0]]
    if missing_columns:
        print(f"⚠️  Colonnes manquantes: {', '.join(missing_columns)}")
    else:
        print("✅ Toutes les colonnes requises sont présentes")

# Test 5: Statistiques
print("\n📈 Test 5: Statistiques des services")
print("-" * 60)
if services:
    prices = [s.get('price_per_lead', 0) for s in services]
    capacities = [s.get('capacity_per_month', 0) for s in services]
    
    print(f"   Prix moyen par lead: {sum(prices) / len(prices):.2f}€")
    print(f"   Prix min: {min(prices)}€")
    print(f"   Prix max: {max(prices)}€")
    print(f"   Capacité moyenne: {sum(capacities) / len(capacities):.0f} leads/mois")
    print(f"   Services disponibles: {sum(1 for s in services if s.get('is_available', True))}")

print("\n" + "=" * 60)
print("✅ TESTS TERMINÉS")
print("=" * 60)
