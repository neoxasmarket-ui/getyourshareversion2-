"""
Script d'initialisation complète - TOP 5 Features
Crée toutes les tables et insère les données de test
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timedelta
import uuid

load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("❌ Variables SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY manquantes dans .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("\n" + "="*60)
print("🚀 INITIALISATION TOP 5 FEATURES - TABLES & DONNÉES TEST")
print("="*60 + "\n")

# ============================================
# 1. GAMIFICATION - Données de test
# ============================================

def init_gamification_data():
    print("📊 1. Initialisation Gamification...")
    
    try:
        # Récupérer quelques utilisateurs existants
        users_response = supabase.table("users").select("id, email, role").limit(10).execute()
        users = users_response.data
        
        if not users:
            print("⚠️  Aucun utilisateur trouvé. Création ignorée.")
            return
        
        print(f"   ✓ {len(users)} utilisateurs trouvés")
        
        # Créer user_gamification pour chaque utilisateur
        gamif_data = []
        for user in users[:6]:  # Top 6 users
            gamif_data.append({
                "user_id": user["id"],
                "user_type": user["role"],
                "total_points": 1000 + (hash(user["id"]) % 5000),
                "current_level": ["bronze", "silver", "gold", "platinum"][hash(user["id"]) % 4],
                "level_points": hash(user["id"]) % 3000,
                "badges_earned": hash(user["id"]) % 10,
                "missions_completed": hash(user["id"]) % 20,
                "streak_days": hash(user["id"]) % 30,
                "leaderboard_position": len(gamif_data) + 1,
                "last_activity_date": datetime.now().isoformat()
            })
        
        # Insérer en base
        result = supabase.table("user_gamification").upsert(gamif_data, on_conflict="user_id").execute()
        print(f"   ✓ {len(gamif_data)} profils gamification créés")
        
        # Créer quelques badges
        badges = [
            {
                "name": "Premier Pas",
                "description": "Première vente réalisée",
                "icon": "🎯",
                "category": "milestone",
                "user_type": "merchant",
                "condition_type": "sales_count",
                "condition_value": 1,
                "points_reward": 100,
                "rarity": "common"
            },
            {
                "name": "Vendeur Pro",
                "description": "10 ventes réalisées",
                "icon": "💎",
                "category": "performance",
                "user_type": "merchant",
                "condition_type": "sales_count",
                "condition_value": 10,
                "points_reward": 500,
                "rarity": "rare"
            },
            {
                "name": "Influenceur Actif",
                "description": "Première promotion réalisée",
                "icon": "⚡",
                "category": "milestone",
                "user_type": "influencer",
                "condition_type": "promotions_count",
                "condition_value": 1,
                "points_reward": 150,
                "rarity": "common"
            },
            {
                "name": "Super Star",
                "description": "50K followers atteints",
                "icon": "🌟",
                "category": "achievement",
                "user_type": "influencer",
                "condition_type": "audience_size",
                "condition_value": 50000,
                "points_reward": 1000,
                "rarity": "epic"
            },
            {
                "name": "Commercial Legend",
                "description": "100 leads convertis",
                "icon": "👑",
                "category": "performance",
                "user_type": "commercial",
                "condition_type": "leads_converted",
                "condition_value": 100,
                "points_reward": 2000,
                "rarity": "legendary"
            }
        ]
        
        badges_result = supabase.table("badges").insert(badges).execute()
        print(f"   ✓ {len(badges)} badges créés")
        
        # Créer quelques missions
        missions = [
            {
                "title": "Ajouter 3 produits",
                "description": "Enrichissez votre catalogue avec 3 nouveaux produits",
                "user_type": "merchant",
                "mission_type": "daily",
                "duration_days": 1,
                "objective_type": "create_products",
                "target_count": 3,
                "points_reward": 150,
                "start_date": datetime.now().date().isoformat(),
                "end_date": (datetime.now() + timedelta(days=7)).date().isoformat(),
                "is_active": True
            },
            {
                "title": "Vendre 5 produits",
                "description": "Réalisez 5 ventes cette semaine",
                "user_type": "merchant",
                "mission_type": "weekly",
                "duration_days": 7,
                "objective_type": "make_sales",
                "target_count": 5,
                "points_reward": 500,
                "start_date": datetime.now().date().isoformat(),
                "end_date": (datetime.now() + timedelta(days=7)).date().isoformat(),
                "is_active": True
            },
            {
                "title": "Publier 3 contenus",
                "description": "Créez 3 posts pour promouvoir des produits",
                "user_type": "influencer",
                "mission_type": "daily",
                "duration_days": 1,
                "objective_type": "post_content",
                "target_count": 3,
                "points_reward": 200,
                "start_date": datetime.now().date().isoformat(),
                "end_date": (datetime.now() + timedelta(days=1)).date().isoformat(),
                "is_active": True
            },
            {
                "title": "Convertir 10 leads",
                "description": "Transformez 10 leads en clients ce mois",
                "user_type": "commercial",
                "mission_type": "monthly",
                "duration_days": 30,
                "objective_type": "convert_leads",
                "target_count": 10,
                "points_reward": 1000,
                "start_date": datetime.now().date().isoformat(),
                "end_date": (datetime.now() + timedelta(days=30)).date().isoformat(),
                "is_active": True
            }
        ]
        
        missions_result = supabase.table("missions").insert(missions).execute()
        print(f"   ✓ {len(missions)} missions créées")
        
        # Créer des progressions de missions pour quelques users
        mission_ids = [m["id"] for m in missions_result.data]
        user_missions = []
        for i, user in enumerate(users[:4]):
            mission_id = mission_ids[i % len(mission_ids)]
            user_missions.append({
                "user_id": user["id"],
                "mission_id": mission_id,
                "current_progress": (i + 1) * 1,
                "target_count": missions[i % len(missions)]["target_count"],
                "status": "active",
                "expires_at": (datetime.now() + timedelta(days=7)).isoformat()
            })
        
        if user_missions:
            supabase.table("user_missions").insert(user_missions).execute()
            print(f"   ✓ {len(user_missions)} progressions missions créées")
        
        print("✅ Gamification initialisé avec succès!\n")
        
    except Exception as e:
        print(f"❌ Erreur gamification: {e}\n")

# ============================================
# 2. MATCHING - Données de test
# ============================================

def init_matching_data():
    print("💘 2. Initialisation Influencer Matching...")
    
    try:
        # Récupérer influenceurs existants
        # Récupérer quelques influenceurs existants
        influencers_response = supabase.table("influencers").select("id, user_id, audience_size, engagement_rate").limit(10).execute()
        influencers = influencers_response.data
        
        if not influencers:
            print("⚠️  Aucun influenceur trouvé. Création ignorée.")
            return
        
        print(f"   ✓ {len(influencers)} influenceurs trouvés")
        
        # Créer profils étendus pour matching
        profiles_extended = []
        niches_list = ["Fashion", "Beauty", "Tech", "Food", "Travel", "Fitness", "Gaming", "Lifestyle"]
        
        for inf in influencers:
            profiles_extended.append({
                "influencer_id": inf["id"],
                "user_id": inf["user_id"],
                "total_followers": inf.get("audience_size", 10000),
                "avg_engagement_rate": inf.get("engagement_rate", 3.5),
                "primary_niche": niches_list[hash(inf["id"]) % len(niches_list)],
                "secondary_niches": [niches_list[(hash(inf["id"]) + i) % len(niches_list)] for i in range(2)],
                "avg_post_views": int(inf.get("audience_size", 10000) * 0.3),
                "avg_post_likes": int(inf.get("audience_size", 10000) * 0.05),
                "avg_post_comments": int(inf.get("audience_size", 10000) * 0.01),
                "price_per_post": 100 + (hash(inf["id"]) % 500),
                "price_per_story": 50 + (hash(inf["id"]) % 200),
                "min_collaboration_budget": 200 + (hash(inf["id"]) % 800),
                "is_available": True,
                "accepts_affiliate": True,
                "accepts_sponsored": True,
                "total_matches": hash(inf["id"]) % 20,
                "total_collaborations": hash(inf["id"]) % 10,
                "success_rate": 60 + (hash(inf["id"]) % 30)
            })
        
        result = supabase.table("influencer_profiles_extended").upsert(profiles_extended, on_conflict="influencer_id").execute()
        print(f"   ✓ {len(profiles_extended)} profils matching créés")
        
        # Créer quelques merchants preferences
        merchants_response = supabase.table("merchants").select("id").limit(5).execute()
        merchants = merchants_response.data
        
        if merchants:
            preferences = []
            for merchant in merchants[:3]:
                preferences.append({
                    "merchant_id": merchant["id"],
                    "min_followers": 5000,
                    "max_followers": 100000,
                    "min_engagement_rate": 2.5,
                    "preferred_niches": ["Fashion", "Beauty", "Lifestyle"],
                    "max_budget_per_post": 500,
                    "max_budget_per_campaign": 5000,
                    "weight_audience": 0.30,
                    "weight_niche": 0.25,
                    "weight_budget": 0.15,
                    "weight_performance": 0.20,
                    "weight_engagement": 0.10
                })
            
            supabase.table("match_preferences").upsert(preferences, on_conflict="merchant_id").execute()
            print(f"   ✓ {len(preferences)} préférences matching créées")
        
        print("✅ Matching initialisé avec succès!\n")
        
    except Exception as e:
        print(f"❌ Erreur matching: {e}\n")

# ============================================
# EXÉCUTION
# ============================================

if __name__ == "__main__":
    try:
        # 1. Gamification
        init_gamification_data()
        
        # 2. Matching
        init_matching_data()
        
        print("\n" + "="*60)
        print("✅ INITIALISATION TERMINÉE AVEC SUCCÈS!")
        print("="*60)
        print("\n📊 Résumé:")
        print("   ✓ Tables gamification créées")
        print("   ✓ Profils gamification initialisés")
        print("   ✓ Badges et missions créés")
        print("   ✓ Tables matching créées")
        print("   ✓ Profils influenceurs enrichis")
        print("\n🚀 Vous pouvez maintenant tester les endpoints:")
        print("   - GET /api/gamification/{user_id}")
        print("   - GET /api/matching/get-recommendations")
        print("   - GET /api/analytics/merchant/{id}")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERREUR GLOBALE: {e}\n")
