-- ============================================
-- TABLES GAMIFICATION - Système Complet
-- Pour Marchands, Influenceurs et Commerciaux
-- ============================================

-- Table: user_gamification (stats globales utilisateur)
CREATE TABLE IF NOT EXISTS user_gamification (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_type VARCHAR(20) NOT NULL, -- 'merchant', 'influencer', 'commercial'
    
    -- Points & Niveau
    total_points INTEGER DEFAULT 0,
    current_level VARCHAR(20) DEFAULT 'bronze', -- bronze, silver, gold, platinum, diamond, legend
    level_points INTEGER DEFAULT 0, -- Points dans le niveau actuel
    
    -- Statistiques
    badges_earned INTEGER DEFAULT 0,
    missions_completed INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 0, -- Jours consécutifs d'activité
    last_activity_date TIMESTAMP,
    
    -- Leaderboard
    leaderboard_position INTEGER,
    leaderboard_region VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id)
);

-- Table: badges (définitions des badges disponibles)
CREATE TABLE IF NOT EXISTS badges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(10), -- Emoji ou code icon
    category VARCHAR(50), -- 'performance', 'engagement', 'milestone', 'special'
    user_type VARCHAR(20), -- 'merchant', 'influencer', 'commercial', 'all'
    
    -- Conditions d'obtention
    condition_type VARCHAR(50), -- 'sales_count', 'revenue_amount', 'followers', etc.
    condition_value INTEGER,
    
    -- Récompenses
    points_reward INTEGER DEFAULT 0,
    
    rarity VARCHAR(20) DEFAULT 'common', -- common, rare, epic, legendary
    is_active BOOLEAN DEFAULT true,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: user_badges (badges obtenus par utilisateurs)
CREATE TABLE IF NOT EXISTS user_badges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    badge_id UUID NOT NULL REFERENCES badges(id) ON DELETE CASCADE,
    
    earned_at TIMESTAMP DEFAULT NOW(),
    is_displayed BOOLEAN DEFAULT true, -- Affiché sur le profil
    
    UNIQUE(user_id, badge_id)
);

-- Table: missions (missions quotidiennes/hebdomadaires)
CREATE TABLE IF NOT EXISTS missions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    user_type VARCHAR(20) NOT NULL, -- 'merchant', 'influencer', 'commercial', 'all'
    
    -- Type & Durée
    mission_type VARCHAR(20) DEFAULT 'daily', -- 'daily', 'weekly', 'monthly', 'special'
    duration_days INTEGER DEFAULT 1,
    
    -- Objectif
    objective_type VARCHAR(50), -- 'create_products', 'make_sales', 'post_content', etc.
    target_count INTEGER NOT NULL,
    
    -- Récompenses
    points_reward INTEGER NOT NULL,
    bonus_reward JSONB, -- Récompenses supplémentaires (badge, reduction, etc.)
    
    -- Disponibilité
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT true,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: user_missions (progression utilisateurs sur missions)
CREATE TABLE IF NOT EXISTS user_missions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    mission_id UUID NOT NULL REFERENCES missions(id) ON DELETE CASCADE,
    
    -- Progression
    current_progress INTEGER DEFAULT 0,
    target_count INTEGER NOT NULL,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'completed', 'expired', 'claimed'
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    expires_at TIMESTAMP,
    
    UNIQUE(user_id, mission_id)
);

-- Table: rewards (récompenses disponibles)
CREATE TABLE IF NOT EXISTS rewards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    user_type VARCHAR(20), -- 'merchant', 'influencer', 'commercial', 'all'
    
    -- Coût
    points_cost INTEGER NOT NULL,
    
    -- Type de récompense
    reward_type VARCHAR(50), -- 'commission_discount', 'free_product', 'priority_support', 'feature_unlock'
    reward_value JSONB, -- Détails de la récompense
    
    -- Disponibilité
    quantity_available INTEGER, -- NULL = illimité
    quantity_claimed INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: user_rewards (récompenses réclamées)
CREATE TABLE IF NOT EXISTS user_rewards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reward_id UUID NOT NULL REFERENCES rewards(id) ON DELETE CASCADE,
    
    claimed_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP, -- Certaines récompenses expirent
    is_used BOOLEAN DEFAULT false,
    used_at TIMESTAMP
);

-- Table: points_history (historique des points gagnés/dépensés)
CREATE TABLE IF NOT EXISTS points_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    points_change INTEGER NOT NULL, -- Peut être négatif
    reason VARCHAR(100), -- 'mission_completed', 'badge_earned', 'reward_claimed', etc.
    reference_id UUID, -- ID de la mission/badge/reward
    
    balance_after INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- INDEX POUR PERFORMANCES
-- ============================================

CREATE INDEX idx_user_gamification_user ON user_gamification(user_id);
CREATE INDEX idx_user_gamification_level ON user_gamification(current_level);
CREATE INDEX idx_user_gamification_leaderboard ON user_gamification(leaderboard_position) WHERE leaderboard_position IS NOT NULL;

CREATE INDEX idx_badges_category ON badges(category);
CREATE INDEX idx_badges_user_type ON badges(user_type);

CREATE INDEX idx_user_badges_user ON user_badges(user_id);
CREATE INDEX idx_user_badges_earned ON user_badges(earned_at DESC);

CREATE INDEX idx_missions_type ON missions(mission_type);
CREATE INDEX idx_missions_user_type ON missions(user_type);
CREATE INDEX idx_missions_active ON missions(is_active) WHERE is_active = true;

CREATE INDEX idx_user_missions_user ON user_missions(user_id);
CREATE INDEX idx_user_missions_status ON user_missions(status);

CREATE INDEX idx_rewards_type ON rewards(reward_type);
CREATE INDEX idx_rewards_active ON rewards(is_active) WHERE is_active = true;

CREATE INDEX idx_points_history_user ON points_history(user_id);
CREATE INDEX idx_points_history_date ON points_history(created_at DESC);

-- ============================================
-- TRIGGERS
-- ============================================

-- Trigger: Update updated_at sur user_gamification
CREATE OR REPLACE FUNCTION update_user_gamification_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_user_gamification_timestamp
BEFORE UPDATE ON user_gamification
FOR EACH ROW
EXECUTE FUNCTION update_user_gamification_timestamp();

-- ============================================
-- COMMENTAIRES
-- ============================================

COMMENT ON TABLE user_gamification IS 'Statistiques gamification par utilisateur';
COMMENT ON TABLE badges IS 'Définitions des badges disponibles';
COMMENT ON TABLE user_badges IS 'Badges obtenus par les utilisateurs';
COMMENT ON TABLE missions IS 'Missions quotidiennes/hebdomadaires';
COMMENT ON TABLE user_missions IS 'Progression des utilisateurs sur les missions';
COMMENT ON TABLE rewards IS 'Récompenses disponibles dans le shop';
COMMENT ON TABLE user_rewards IS 'Récompenses réclamées par les utilisateurs';
COMMENT ON TABLE points_history IS 'Historique des mouvements de points';
