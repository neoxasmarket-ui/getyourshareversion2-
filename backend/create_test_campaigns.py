"""
Script pour créer des campagnes de test
"""
import os
from supabase import create_client
from datetime import datetime, timedelta
import uuid
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://tuvgjccfplguagdgigyo.supabase.co")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ SUPABASE_SERVICE_ROLE_KEY non trouvé dans les variables d'environnement")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def get_merchant_ids():
    """Récupérer les IDs des merchants"""
    try:
        response = supabase.table("merchants").select("id, user_id").limit(5).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des merchants: {e}")
        return []

def create_campaigns():
    """Créer des campagnes de test"""
    
    merchants = get_merchant_ids()
    
    if not merchants:
        print("❌ Aucun merchant trouvé dans la base de données")
        return
    
    print(f"✅ {len(merchants)} merchants trouvés\n")
    
    # Campagnes à créer - Adaptées à la structure existante
    # Colonnes disponibles: id, merchant_id, name, description, budget, spent, 
    # start_date, end_date, target_audience, status, total_clicks, total_conversions, 
    # total_revenue, roi, created_at, updated_at
    
    campaigns_data = [
        {
            "name": "Lancement Collection Printemps 2025",
            "description": "Promotion de notre nouvelle collection printemps avec des influenceurs mode. Ciblez les femmes 18-35 ans passionnées de mode et lifestyle. Instagram 10K+ followers requis.",
            "budget": 5000.00,
            "spent": 0.00,
            "status": "active",
            "start_date": datetime.now().date().isoformat(),
            "end_date": (datetime.now() + timedelta(days=30)).date().isoformat(),
            "target_audience": "Femmes 18-35 ans, mode et lifestyle, Instagram 10K+ followers",
            "total_clicks": 0,
            "total_conversions": 0,
            "total_revenue": 0.00,
            "roi": 0.00
        },
        {
            "name": "Promotion Black Friday 2025",
            "description": "Campagne massive pour le Black Friday avec codes promo exclusifs. Tous publics 20-45 ans. Objectif: maximiser les conversions avec une commission attractive de 20%.",
            "budget": 10000.00,
            "spent": 0.00,
            "status": "active",
            "start_date": datetime.now().date().isoformat(),
            "end_date": (datetime.now() + timedelta(days=15)).date().isoformat(),
            "target_audience": "Shoppers 20-45 ans, toutes catégories, Instagram/TikTok 5K+",
            "total_clicks": 0,
            "total_conversions": 0,
            "total_revenue": 0.00,
            "roi": 0.00
        },
        {
            "name": "Campagne Beauté - Cosmétiques Bio",
            "description": "Lancement d'une gamme de cosmétiques naturels et bio. Recherche micro-influenceurs beauté authentiques avec engagement élevé. Focus sur l'aspect naturel et eco-friendly.",
            "budget": 3000.00,
            "spent": 0.00,
            "status": "active",
            "start_date": datetime.now().date().isoformat(),
            "end_date": (datetime.now() + timedelta(days=45)).date().isoformat(),
            "target_audience": "Femmes 25-40 ans, beauté naturelle, micro-influenceurs 3K+",
            "total_clicks": 0,
            "total_conversions": 0,
            "total_revenue": 0.00,
            "roi": 0.00
        },
        {
            "name": "Challenge Fitness #TransformationMaroc",
            "description": "Challenge fitness de 30 jours avec nos équipements sportifs. Programme de transformation complet. Influenceurs fitness motivants recherchés pour inspirer la communauté marocaine.",
            "budget": 4000.00,
            "spent": 0.00,
            "status": "active",
            "start_date": datetime.now().date().isoformat(),
            "end_date": (datetime.now() + timedelta(days=60)).date().isoformat(),
            "target_audience": "Hommes et femmes 20-35 ans, fitness et santé, 5K+ followers",
            "total_clicks": 0,
            "total_conversions": 0,
            "total_revenue": 0.00,
            "roi": 0.00
        },
        {
            "name": "Ramadan 2025 - Collection Spéciale",
            "description": "Collection spéciale Ramadan: produits alimentaires, décorations, tenues traditionnelles. Campagne culturelle ciblant les familles marocaines. Contenu authentique et respectueux.",
            "budget": 7000.00,
            "spent": 0.00,
            "status": "draft",
            "start_date": (datetime.now() + timedelta(days=60)).date().isoformat(),
            "end_date": (datetime.now() + timedelta(days=90)).date().isoformat(),
            "target_audience": "Familles marocaines 25-50 ans, lifestyle, 8K+ followers",
            "total_clicks": 0,
            "total_conversions": 0,
            "total_revenue": 0.00,
            "roi": 0.00
        },
        {
            "name": "Tech Gadgets - Rentrée Universitaire",
            "description": "Promotion gadgets technologiques pour étudiants et jeunes professionnels: laptops, tablettes, accessoires. Reviews et comparatifs demandés. Public tech-savvy.",
            "budget": 6000.00,
            "spent": 0.00,
            "status": "paused",
            "start_date": (datetime.now() - timedelta(days=10)).date().isoformat(),
            "end_date": (datetime.now() + timedelta(days=20)).date().isoformat(),
            "target_audience": "Étudiants et professionnels 18-30 ans, tech, 7K+ followers",
            "total_clicks": 0,
            "total_conversions": 0,
            "total_revenue": 0.00,
            "roi": 0.00
        }
    ]
    
    created_count = 0
    
    for i, campaign_data in enumerate(campaigns_data):
        # Assigner à un merchant différent (rotation)
        merchant = merchants[i % len(merchants)]
        campaign_data["merchant_id"] = merchant["id"]
        campaign_data["created_at"] = datetime.now().isoformat()
        campaign_data["updated_at"] = datetime.now().isoformat()
        
        try:
            response = supabase.table("campaigns").insert(campaign_data).execute()
            
            if response.data:
                created_count += 1
                status_emoji = "🟢" if campaign_data["status"] == "active" else "⏸️" if campaign_data["status"] == "paused" else "📝"
                
                print(f"{status_emoji} {campaign_data['name']}")
                print(f"   Budget: {campaign_data['budget']} MAD | Dépensé: {campaign_data['spent']} MAD")
                print(f"   Période: {campaign_data['start_date']} → {campaign_data['end_date']}")
                print(f"   Statut: {campaign_data['status']} | Merchant: {merchant['id'][:8]}...\n")
            
        except Exception as e:
            print(f"❌ Erreur création '{campaign_data['name']}': {e}\n")
            continue
    
    print(f"\n{'='*60}")
    print(f"✅ {created_count}/{len(campaigns_data)} CAMPAGNES CRÉÉES AVEC SUCCÈS!")
    print(f"{'='*60}\n")
    
    # Récapitulatif
    print("📊 RÉCAPITULATIF:")
    print(f"   🟢 Actives: {sum(1 for c in campaigns_data[:created_count] if c['status'] == 'active')}")
    print(f"   📝 Brouillons: {sum(1 for c in campaigns_data[:created_count] if c['status'] == 'draft')}")
    print(f"   ⏸️  Pausées: {sum(1 for c in campaigns_data[:created_count] if c['status'] == 'paused')}")
    print(f"\n🌐 Accédez à: http://localhost:3000/campaigns")
    print("📝 Rafraîchissez la page pour voir les nouvelles campagnes!")
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎯 CRÉATION DE CAMPAGNES DE TEST")
    print("="*60 + "\n")
    
    create_campaigns()
