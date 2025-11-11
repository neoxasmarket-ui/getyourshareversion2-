-- ============================================
-- TABLES INFLUENCER MATCHING - Système Tinder
-- ============================================

-- Table: influencer_profiles_extended (profils enrichis pour matching)
CREATE TABLE IF NOT EXISTS influencer_profiles_extended (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    influencer_id UUID NOT NULL REFERENCES influencers(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Audience
    total_followers INTEGER DEFAULT 0,
    avg_engagement_rate DECIMAL(5,2) DEFAULT 0.00, -- Pourcentage
    audience_demographics JSONB, -- {age_ranges, gender, locations}
    
    -- Niches & Intérêts
    primary_niche VARCHAR(100),
    secondary_niches TEXT[], -- Array de niches
    interests TEXT[], -- Array d'intérêts
    
    -- Performance
    avg_post_views INTEGER DEFAULT 0,
    avg_post_likes INTEGER DEFAULT 0,
    avg_post_comments INTEGER DEFAULT 0,
    avg_story_views INTEGER DEFAULT 0,
    
    -- Budget & Prix
    price_per_post DECIMAL(10,2),
    price_per_story DECIMAL(10,2),
    price_per_video DECIMAL(10,2),
    min_collaboration_budget DECIMAL(10,2),
    
    -- Disponibilité
    is_available BOOLEAN DEFAULT true,
    accepts_affiliate BOOLEAN DEFAULT true,
    accepts_sponsored BOOLEAN DEFAULT true,
    preferred_brands TEXT[], -- Array de marques préférées
    
    -- Statistiques matching
    total_matches INTEGER DEFAULT 0,
    total_collaborations INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2) DEFAULT 0.00,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(influencer_id),
    UNIQUE(user_id)
);

-- Table: matching_swipes (historique des swipes)
CREATE TABLE IF NOT EXISTS matching_swipes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    merchant_id UUID NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    influencer_id UUID NOT NULL REFERENCES influencers(id) ON DELETE CASCADE,
    
    -- Action
    swipe_action VARCHAR(20) NOT NULL, -- 'like', 'pass', 'super_like'
    swipe_direction VARCHAR(10), -- 'right', 'left' (pour UI)
    
    -- Score de match (calculé par l'algorithme)
    match_score INTEGER, -- 0-100
    match_factors JSONB, -- Détails du scoring {audience: 85, niche: 90, budget: 70, etc.}
    
    -- Mutual match
    is_mutual_match BOOLEAN DEFAULT false,
    matched_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(merchant_id, influencer_id)
);

-- Table: matches (matches confirmés)
CREATE TABLE IF NOT EXISTS matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    merchant_id UUID NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    influencer_id UUID NOT NULL REFERENCES influencers(id) ON DELETE CASCADE,
    
    -- Score de match
    match_score INTEGER NOT NULL,
    match_quality VARCHAR(20), -- 'excellent', 'good', 'average'
    
    -- Estimations
    estimated_reach INTEGER,
    estimated_engagement INTEGER,
    estimated_conversions INTEGER,
    estimated_roi DECIMAL(10,2),
    
    -- Communication
    conversation_id UUID, -- Référence à une conversation
    first_message_sent BOOLEAN DEFAULT false,
    
    -- Status
    status VARCHAR(20) DEFAULT 'new', -- 'new', 'contacted', 'negotiating', 'accepted', 'rejected', 'completed'
    
    matched_at TIMESTAMP DEFAULT NOW(),
    last_interaction_at TIMESTAMP,
    expires_at TIMESTAMP, -- Les matches expirent après X jours
    
    UNIQUE(merchant_id, influencer_id)
);

-- Table: match_preferences (préférences de matching par marchand)
CREATE TABLE IF NOT EXISTS match_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    merchant_id UUID NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    
    -- Filtres
    min_followers INTEGER,
    max_followers INTEGER,
    min_engagement_rate DECIMAL(5,2),
    preferred_niches TEXT[],
    excluded_niches TEXT[],
    
    -- Budget
    max_budget_per_post DECIMAL(10,2),
    max_budget_per_campaign DECIMAL(10,2),
    
    -- Géographie
    preferred_locations TEXT[], -- Array de pays/villes
    
    -- Algorithme weights
    weight_audience DECIMAL(3,2) DEFAULT 0.30, -- 30%
    weight_niche DECIMAL(3,2) DEFAULT 0.25, -- 25%
    weight_budget DECIMAL(3,2) DEFAULT 0.15, -- 15%
    weight_performance DECIMAL(3,2) DEFAULT 0.20, -- 20%
    weight_engagement DECIMAL(3,2) DEFAULT 0.10, -- 10%
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(merchant_id)
);

-- ============================================
-- INDEX POUR PERFORMANCES
-- ============================================

CREATE INDEX idx_influencer_profiles_ext_influencer ON influencer_profiles_extended(influencer_id);
CREATE INDEX idx_influencer_profiles_ext_available ON influencer_profiles_extended(is_available) WHERE is_available = true;
CREATE INDEX idx_influencer_profiles_ext_followers ON influencer_profiles_extended(total_followers);
CREATE INDEX idx_influencer_profiles_ext_engagement ON influencer_profiles_extended(avg_engagement_rate);
CREATE INDEX idx_influencer_profiles_ext_niche ON influencer_profiles_extended(primary_niche);

CREATE INDEX idx_matching_swipes_merchant ON matching_swipes(merchant_id);
CREATE INDEX idx_matching_swipes_influencer ON matching_swipes(influencer_id);
CREATE INDEX idx_matching_swipes_action ON matching_swipes(swipe_action);
CREATE INDEX idx_matching_swipes_mutual ON matching_swipes(is_mutual_match) WHERE is_mutual_match = true;

CREATE INDEX idx_matches_merchant ON matches(merchant_id);
CREATE INDEX idx_matches_influencer ON matches(influencer_id);
CREATE INDEX idx_matches_status ON matches(status);
CREATE INDEX idx_matches_quality ON matches(match_quality);
CREATE INDEX idx_matches_date ON matches(matched_at DESC);

CREATE INDEX idx_match_preferences_merchant ON match_preferences(merchant_id);

-- ============================================
-- TRIGGERS
-- ============================================

-- Trigger: Update updated_at
CREATE OR REPLACE FUNCTION update_matching_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_influencer_profiles_timestamp
BEFORE UPDATE ON influencer_profiles_extended
FOR EACH ROW
EXECUTE FUNCTION update_matching_timestamp();

CREATE TRIGGER trigger_update_match_preferences_timestamp
BEFORE UPDATE ON match_preferences
FOR EACH ROW
EXECUTE FUNCTION update_matching_timestamp();

-- ============================================
-- COMMENTAIRES
-- ============================================

COMMENT ON TABLE influencer_profiles_extended IS 'Profils enrichis des influenceurs pour matching';
COMMENT ON TABLE matching_swipes IS 'Historique des swipes Tinder-style';
COMMENT ON TABLE matches IS 'Matches confirmés entre marchands et influenceurs';
COMMENT ON TABLE match_preferences IS 'Préférences de matching par marchand';
