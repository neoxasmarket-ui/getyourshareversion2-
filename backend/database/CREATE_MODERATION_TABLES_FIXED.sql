-- ============================================
-- TABLE DE MODÉRATION DES PRODUITS
-- Version fixée sans références strictes
-- ============================================

-- Table principale de modération
CREATE TABLE IF NOT EXISTS moderation_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Référence au produit (nullable car produit pas encore créé)
    product_id UUID,
    merchant_id UUID,
    user_id UUID,
    
    -- Données du produit au moment de la soumission
    product_name VARCHAR(255) NOT NULL,
    product_description TEXT NOT NULL,
    product_category VARCHAR(100),
    product_price DECIMAL(10, 2),
    product_images JSONB, -- URLs des images
    
    -- Résultat de la modération IA
    status VARCHAR(50) DEFAULT 'pending',
    ai_decision VARCHAR(20), -- 'approved' ou 'rejected'
    ai_confidence DECIMAL(3, 2), -- 0.00 à 1.00
    ai_risk_level VARCHAR(20), -- 'low', 'medium', 'high', 'critical'
    ai_flags JSONB, -- Array des catégories détectées
    ai_reason TEXT, -- Raison du rejet par l'IA
    ai_recommendation TEXT,
    moderation_method VARCHAR(20), -- 'ai' ou 'keywords'
    
    -- Décision admin
    admin_decision VARCHAR(20), -- 'approved' ou 'rejected'
    admin_user_id UUID,
    admin_comment TEXT,
    reviewed_at TIMESTAMP,
    
    -- Metadata
    submission_attempts INT DEFAULT 1,
    priority INT DEFAULT 0, -- Plus élevé = plus prioritaire
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index pour performance
CREATE INDEX IF NOT EXISTS idx_moderation_status ON moderation_queue(status);
CREATE INDEX IF NOT EXISTS idx_moderation_merchant ON moderation_queue(merchant_id);
CREATE INDEX IF NOT EXISTS idx_moderation_created ON moderation_queue(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_moderation_priority ON moderation_queue(priority DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_moderation_risk ON moderation_queue(ai_risk_level);

-- ============================================
-- TABLE DES STATS DE MODÉRATION
-- ============================================

CREATE TABLE IF NOT EXISTS moderation_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE DEFAULT CURRENT_DATE,
    
    -- Compteurs
    total_submissions INT DEFAULT 0,
    ai_approved INT DEFAULT 0,
    ai_rejected INT DEFAULT 0,
    admin_approved INT DEFAULT 0,
    admin_rejected INT DEFAULT 0,
    pending INT DEFAULT 0,
    
    -- Flags par catégorie
    flags_adult_content INT DEFAULT 0,
    flags_weapons INT DEFAULT 0,
    flags_drugs INT DEFAULT 0,
    flags_gambling INT DEFAULT 0,
    flags_counterfeit INT DEFAULT 0,
    flags_illegal INT DEFAULT 0,
    flags_other INT DEFAULT 0,
    
    -- Performance
    avg_ai_confidence DECIMAL(3, 2),
    avg_review_time_minutes INT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(date)
);

-- Index pour stats
CREATE INDEX IF NOT EXISTS idx_moderation_stats_date ON moderation_stats(date DESC);

-- ============================================
-- HISTORIQUE DES DÉCISIONS
-- ============================================

CREATE TABLE IF NOT EXISTS moderation_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    moderation_id UUID,
    
    action VARCHAR(50) NOT NULL, -- 'submitted', 'ai_reviewed', 'admin_approved', 'admin_rejected'
    performed_by UUID,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    comment TEXT,
    metadata JSONB,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_moderation_history_mod ON moderation_history(moderation_id);
CREATE INDEX IF NOT EXISTS idx_moderation_history_date ON moderation_history(created_at DESC);

-- ============================================
-- VUES UTILES
-- ============================================

-- Vue des produits en attente de révision admin
CREATE OR REPLACE VIEW v_pending_moderation AS
SELECT 
    mq.*,
    m.company_name as merchant_name,
    u_merchant.email as merchant_email,
    u.email as user_email,
    EXTRACT(EPOCH FROM (NOW() - mq.created_at))/3600 as hours_pending,
    CASE 
        WHEN ai_risk_level = 'critical' THEN 1
        WHEN ai_risk_level = 'high' THEN 2
        WHEN ai_risk_level = 'medium' THEN 3
        ELSE 4
    END as risk_priority
FROM moderation_queue mq
LEFT JOIN merchants m ON mq.merchant_id = m.id
LEFT JOIN users u_merchant ON m.user_id = u_merchant.id
LEFT JOIN users u ON mq.user_id = u.id
WHERE mq.status = 'pending'
ORDER BY risk_priority ASC, mq.created_at ASC;

-- Vue des stats quotidiennes
CREATE OR REPLACE VIEW v_daily_moderation_stats AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE ai_decision = 'approved') as ai_approved,
    COUNT(*) FILTER (WHERE ai_decision = 'rejected') as ai_rejected,
    COUNT(*) FILTER (WHERE status = 'pending') as pending,
    COUNT(*) FILTER (WHERE status = 'approved') as admin_approved,
    COUNT(*) FILTER (WHERE status = 'rejected') as admin_rejected,
    AVG(ai_confidence) as avg_confidence,
    AVG(EXTRACT(EPOCH FROM (reviewed_at - created_at))/60) FILTER (WHERE reviewed_at IS NOT NULL) as avg_review_minutes
FROM moderation_queue
GROUP BY DATE(created_at)
ORDER BY date DESC;
