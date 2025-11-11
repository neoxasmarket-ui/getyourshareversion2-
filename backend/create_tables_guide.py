"""
Script Master - Création complète des tables TOP 5
Exécute les SQL via l'API Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("❌ Variables SUPABASE_URL et SUPABASE_KEY manquantes")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("\n" + "="*60)
print("🗄️  CRÉATION TABLES TOP 5 FEATURES")
print("="*60 + "\n")

# ============================================
# GAMIFICATION TABLES
# ============================================

GAMIFICATION_SQL = """
-- Table: user_gamification
CREATE TABLE IF NOT EXISTS user_gamification (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_type VARCHAR(20) NOT NULL,
    total_points INTEGER DEFAULT 0,
    current_level VARCHAR(20) DEFAULT 'bronze',
    level_points INTEGER DEFAULT 0,
    badges_earned INTEGER DEFAULT 0,
    missions_completed INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 0,
    last_activity_date TIMESTAMP,
    leaderboard_position INTEGER,
    leaderboard_region VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Table: badges
CREATE TABLE IF NOT EXISTS badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(10),
    category VARCHAR(50),
    user_type VARCHAR(20),
    condition_type VARCHAR(50),
    condition_value INTEGER,
    points_reward INTEGER DEFAULT 0,
    rarity VARCHAR(20) DEFAULT 'common',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: user_badges
CREATE TABLE IF NOT EXISTS user_badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    badge_id UUID NOT NULL REFERENCES badges(id) ON DELETE CASCADE,
    earned_at TIMESTAMP DEFAULT NOW(),
    is_displayed BOOLEAN DEFAULT true,
    UNIQUE(user_id, badge_id)
);

-- Table: missions
CREATE TABLE IF NOT EXISTS missions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    user_type VARCHAR(20) NOT NULL,
    mission_type VARCHAR(20) DEFAULT 'daily',
    duration_days INTEGER DEFAULT 1,
    objective_type VARCHAR(50),
    target_count INTEGER NOT NULL,
    points_reward INTEGER NOT NULL,
    bonus_reward JSONB,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: user_missions
CREATE TABLE IF NOT EXISTS user_missions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    mission_id UUID NOT NULL REFERENCES missions(id) ON DELETE CASCADE,
    current_progress INTEGER DEFAULT 0,
    target_count INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    expires_at TIMESTAMP,
    UNIQUE(user_id, mission_id)
);

-- Table: rewards
CREATE TABLE IF NOT EXISTS rewards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    user_type VARCHAR(20),
    points_cost INTEGER NOT NULL,
    reward_type VARCHAR(50),
    reward_value JSONB,
    quantity_available INTEGER,
    quantity_claimed INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: user_rewards
CREATE TABLE IF NOT EXISTS user_rewards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reward_id UUID NOT NULL REFERENCES rewards(id) ON DELETE CASCADE,
    claimed_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    is_used BOOLEAN DEFAULT false,
    used_at TIMESTAMP
);

-- Table: points_history
CREATE TABLE IF NOT EXISTS points_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    points_change INTEGER NOT NULL,
    reason VARCHAR(100),
    reference_id UUID,
    balance_after INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
"""

# ============================================
# MATCHING TABLES
# ============================================

MATCHING_SQL = """
-- Table: influencer_profiles_extended
CREATE TABLE IF NOT EXISTS influencer_profiles_extended (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    influencer_id UUID NOT NULL REFERENCES influencers(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total_followers INTEGER DEFAULT 0,
    avg_engagement_rate DECIMAL(5,2) DEFAULT 0.00,
    audience_demographics JSONB,
    primary_niche VARCHAR(100),
    secondary_niches TEXT[],
    interests TEXT[],
    avg_post_views INTEGER DEFAULT 0,
    avg_post_likes INTEGER DEFAULT 0,
    avg_post_comments INTEGER DEFAULT 0,
    avg_story_views INTEGER DEFAULT 0,
    price_per_post DECIMAL(10,2),
    price_per_story DECIMAL(10,2),
    price_per_video DECIMAL(10,2),
    min_collaboration_budget DECIMAL(10,2),
    is_available BOOLEAN DEFAULT true,
    accepts_affiliate BOOLEAN DEFAULT true,
    accepts_sponsored BOOLEAN DEFAULT true,
    preferred_brands TEXT[],
    total_matches INTEGER DEFAULT 0,
    total_collaborations INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(influencer_id),
    UNIQUE(user_id)
);

-- Table: matching_swipes
CREATE TABLE IF NOT EXISTS matching_swipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    influencer_id UUID NOT NULL REFERENCES influencers(id) ON DELETE CASCADE,
    swipe_action VARCHAR(20) NOT NULL,
    swipe_direction VARCHAR(10),
    match_score INTEGER,
    match_factors JSONB,
    is_mutual_match BOOLEAN DEFAULT false,
    matched_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(merchant_id, influencer_id)
);

-- Table: matches
CREATE TABLE IF NOT EXISTS matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    influencer_id UUID NOT NULL REFERENCES influencers(id) ON DELETE CASCADE,
    match_score INTEGER NOT NULL,
    match_quality VARCHAR(20),
    estimated_reach INTEGER,
    estimated_engagement INTEGER,
    estimated_conversions INTEGER,
    estimated_roi DECIMAL(10,2),
    conversation_id UUID,
    first_message_sent BOOLEAN DEFAULT false,
    status VARCHAR(20) DEFAULT 'new',
    matched_at TIMESTAMP DEFAULT NOW(),
    last_interaction_at TIMESTAMP,
    expires_at TIMESTAMP,
    UNIQUE(merchant_id, influencer_id)
);

-- Table: match_preferences
CREATE TABLE IF NOT EXISTS match_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    min_followers INTEGER,
    max_followers INTEGER,
    min_engagement_rate DECIMAL(5,2),
    preferred_niches TEXT[],
    excluded_niches TEXT[],
    max_budget_per_post DECIMAL(10,2),
    max_budget_per_campaign DECIMAL(10,2),
    preferred_locations TEXT[],
    weight_audience DECIMAL(3,2) DEFAULT 0.30,
    weight_niche DECIMAL(3,2) DEFAULT 0.25,
    weight_budget DECIMAL(3,2) DEFAULT 0.15,
    weight_performance DECIMAL(3,2) DEFAULT 0.20,
    weight_engagement DECIMAL(3,2) DEFAULT 0.10,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(merchant_id)
);
"""

print("📊 Étape 1/2: Création tables Gamification...")
try:
    # Note: Supabase Python client ne supporte pas directement l'exécution de SQL
    # Il faut utiliser les fonctions RPC ou créer via le dashboard
    print("⚠️  Les tables doivent être créées manuellement via le dashboard Supabase")
    print("   Ou via SQL Editor dans Supabase Dashboard")
    print("\n   📝 Fichiers SQL disponibles:")
    print("      - CREATE_GAMIFICATION_TABLES.sql")
    print("      - CREATE_MATCHING_TABLES.sql")
    print("\n   💡 Instructions:")
    print("      1. Ouvrez Supabase Dashboard")
    print("      2. Allez dans 'SQL Editor'")
    print("      3. Copiez-collez le contenu des fichiers .sql")
    print("      4. Exécutez les requêtes")
    print("\n   ⏭️  Une fois fait, exécutez: python init_top5_data.py")
    
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "="*60)
print("ℹ️  PROCHAINE ÉTAPE")
print("="*60)
print("\n1. Créez les tables via Supabase Dashboard (SQL Editor)")
print("2. Puis exécutez: python init_top5_data.py")
print("\n")
