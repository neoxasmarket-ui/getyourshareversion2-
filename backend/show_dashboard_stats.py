#!/usr/bin/env python3
"""
Affichage visuel des statistiques du dashboard admin
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db_helpers import get_dashboard_stats
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://jmehgebizhfabgjgflkd.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImptZWhnZWJpemhmYWJnamdmbGtkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyMzU1ODUwOCwiZXhwIjoyMDM5MTM0NTA4fQ.pGIkBIw4qzaBT9d4BEVwdipKlLrjc52qsxmCPOCmBus")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Récupérer un admin ID
admin_result = supabase.table("users").select("id").eq("role", "admin").limit(1).execute()
admin_id = admin_result.data[0]["id"] if admin_result.data else None

# Récupérer les stats
stats = get_dashboard_stats("admin", admin_id)

# Affichage stylé
print("\n" + "=" * 80)
print(" " * 25 + "🎯 DASHBOARD ADMIN - STATISTIQUES")
print("=" * 80)

# Cartes de stats principales
cards = [
    ("💰", "Revenus Total", f"{stats.get('total_revenue', 0):,.2f} €", "green"),
    ("🏪", "Entreprises", f"{stats.get('total_merchants', 0)}", "indigo"),
    ("🌟", "Influenceurs", f"{stats.get('total_influencers', 0)}", "purple"),
    ("📦", "Produits", f"{stats.get('total_products', 0)}", "orange"),
    ("💼", "Services", f"{stats.get('total_services', 0)}", "teal"),
]

print("\n┌" + "─" * 78 + "┐")
for icon, title, value, color in cards:
    spaces = 60 - len(title) - len(value)
    print(f"│ {icon}  {title}:" + " " * spaces + f"{value:>12} │")
print("└" + "─" * 78 + "┘")

# Détails supplémentaires
print("\n📊 DÉTAILS:")
print("─" * 80)
print(f"   Total utilisateurs dans la plateforme: {stats.get('total_users', 0)}")

# Calculs de pourcentages
total_users = stats.get('total_users', 0)
if total_users > 0:
    merchants_pct = (stats.get('total_merchants', 0) / total_users) * 100
    influencers_pct = (stats.get('total_influencers', 0) / total_users) * 100
    print(f"   Pourcentage d'entreprises: {merchants_pct:.1f}%")
    print(f"   Pourcentage d'influenceurs: {influencers_pct:.1f}%")

# Moyennes
total_merchants = stats.get('total_merchants', 0)
if total_merchants > 0:
    avg_products = stats.get('total_products', 0) / total_merchants
    avg_services = stats.get('total_services', 0) / total_merchants
    print(f"\n   Moyenne de produits par entreprise: {avg_products:.1f}")
    print(f"   Moyenne de services par entreprise: {avg_services:.1f}")

# État de la plateforme
print("\n🚀 ÉTAT DE LA PLATEFORME:")
print("─" * 80)

total_offers = stats.get('total_products', 0) + stats.get('total_services', 0)
print(f"   Total d'offres disponibles: {total_offers} (Produits + Services)")

if stats.get('total_revenue', 0) > 0:
    print(f"   Plateforme génératrice de revenus: ✅ Active")
else:
    print(f"   Plateforme génératrice de revenus: ⚠️  En attente de premières ventes")

print("\n" + "=" * 80)
print(" " * 30 + "✅ Dashboard prêt à l'emploi!")
print("=" * 80 + "\n")
