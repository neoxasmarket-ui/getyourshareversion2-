-- ============================================================================
-- MIGRATION: Ajout du système Commercial (Sales Representatives)
-- Description: Ajoute les commerciaux comme intervenant dépendant avec tableau de bord
-- Date: 2025-11-09
-- ============================================================================

-- 1. Ajouter le rôle 'commercial' aux utilisateurs
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'customer';

-- Mettre à jour la contrainte pour inclure 'commercial'
ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check;
ALTER TABLE users ADD CONSTRAINT users_role_check
  CHECK (role IN ('customer', 'merchant', 'influencer', 'commercial', 'admin'));

-- 2. Créer la table des profils commerciaux
CREATE TABLE IF NOT EXISTS sales_representatives (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

  -- Informations professionnelles
  employee_id VARCHAR(50) UNIQUE,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(20),

  -- Statut et niveau
  status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended', 'training')),
  level VARCHAR(20) DEFAULT 'junior' CHECK (level IN ('trainee', 'junior', 'senior', 'team_lead', 'manager')),

  -- Hiérarchie (rattachement)
  manager_id UUID REFERENCES sales_representatives(id),
  team_id UUID,
  territory VARCHAR(100), -- Casablanca, Rabat, Marrakech, etc.

  -- Informations de performance
  hire_date DATE NOT NULL DEFAULT CURRENT_DATE,
  total_deals INTEGER DEFAULT 0,
  total_revenue DECIMAL(12, 2) DEFAULT 0,
  conversion_rate DECIMAL(5, 2) DEFAULT 0, -- Pourcentage
  average_deal_value DECIMAL(12, 2) DEFAULT 0,

  -- Gamification
  points INTEGER DEFAULT 0,
  level_tier VARCHAR(20) DEFAULT 'bronze' CHECK (level_tier IN ('bronze', 'silver', 'gold', 'platinum', 'diamond', 'legend')),
  badges JSONB DEFAULT '[]',
  achievements JSONB DEFAULT '[]',

  -- Commission & Rémunération
  commission_rate DECIMAL(5, 2) DEFAULT 3.00, -- % par défaut
  commission_earned DECIMAL(12, 2) DEFAULT 0,
  commission_paid DECIMAL(12, 2) DEFAULT 0,
  commission_pending DECIMAL(12, 2) DEFAULT 0,

  -- Métadonnées
  metadata JSONB DEFAULT '{}',
  settings JSONB DEFAULT '{}',

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_login_at TIMESTAMP WITH TIME ZONE,

  CONSTRAINT unique_user_sales_rep UNIQUE (user_id)
);

-- 3. Créer la table des leads/prospects (pour commerciaux)
CREATE TABLE IF NOT EXISTS sales_leads (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Assignment
  sales_rep_id UUID REFERENCES sales_representatives(id) ON DELETE SET NULL,
  assigned_at TIMESTAMP WITH TIME ZONE,
  assigned_by UUID REFERENCES users(id),

  -- Informations du lead
  company_name VARCHAR(255),
  contact_name VARCHAR(255) NOT NULL,
  contact_email VARCHAR(255),
  contact_phone VARCHAR(20),
  position VARCHAR(100),

  -- Détails
  industry VARCHAR(100),
  company_size VARCHAR(50), -- '1-10', '11-50', '51-200', '201-1000', '1000+'
  location VARCHAR(255),

  -- Qualification
  lead_source VARCHAR(50), -- 'inbound', 'outbound', 'referral', 'event', 'partner'
  lead_status VARCHAR(50) DEFAULT 'new' CHECK (lead_status IN (
    'new', 'contacted', 'qualified', 'proposal', 'negotiation',
    'closed_won', 'closed_lost', 'on_hold', 'nurturing'
  )),

  -- Scoring IA
  score INTEGER DEFAULT 0 CHECK (score >= 0 AND score <= 100),
  score_factors JSONB DEFAULT '{}', -- Détails du scoring
  probability_to_close DECIMAL(5, 2) DEFAULT 0, -- %

  -- Valeur estimée
  estimated_value DECIMAL(12, 2),
  estimated_commission DECIMAL(12, 2),
  expected_close_date DATE,

  -- Produit/Service d'intérêt
  product_interest VARCHAR(255),
  service_interest VARCHAR(255),
  budget_range VARCHAR(50),

  -- Activité
  last_contact_date TIMESTAMP WITH TIME ZONE,
  next_follow_up_date TIMESTAMP WITH TIME ZONE,
  contact_count INTEGER DEFAULT 0,

  -- Notes et historique
  notes TEXT,
  activity_log JSONB DEFAULT '[]',
  tags JSONB DEFAULT '[]',

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  closed_at TIMESTAMP WITH TIME ZONE
);

-- 4. Créer la table des deals (ventes fermées)
CREATE TABLE IF NOT EXISTS sales_deals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Références
  lead_id UUID REFERENCES sales_leads(id),
  sales_rep_id UUID NOT NULL REFERENCES sales_representatives(id),
  merchant_id UUID REFERENCES merchants(id),

  -- Informations du deal
  deal_name VARCHAR(255) NOT NULL,
  deal_type VARCHAR(50) CHECK (deal_type IN ('product_commission', 'service_fixed', 'recurring', 'one_time')),

  -- Montants
  deal_value DECIMAL(12, 2) NOT NULL,
  commission_rate DECIMAL(5, 2),
  commission_amount DECIMAL(12, 2) NOT NULL,

  -- Produit ou Service
  product_id UUID, -- Si vente de produit
  service_name VARCHAR(255), -- Si vente de service
  quantity INTEGER DEFAULT 1,

  -- Statut
  status VARCHAR(50) DEFAULT 'pending' CHECK (status IN (
    'pending', 'approved', 'delivered', 'completed', 'cancelled', 'refunded'
  )),

  -- Paiement commission
  commission_status VARCHAR(50) DEFAULT 'pending' CHECK (commission_status IN (
    'pending', 'approved', 'paid', 'held', 'cancelled'
  )),
  paid_at TIMESTAMP WITH TIME ZONE,
  payment_reference VARCHAR(255),

  -- Détails
  contract_url VARCHAR(500),
  invoice_url VARCHAR(500),
  notes TEXT,
  metadata JSONB DEFAULT '{}',

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  closed_at TIMESTAMP WITH TIME ZONE,

  CONSTRAINT positive_deal_value CHECK (deal_value > 0),
  CONSTRAINT positive_commission CHECK (commission_amount >= 0)
);

-- 5. Créer la table des activités commerciales (call logs, emails, meetings)
CREATE TABLE IF NOT EXISTS sales_activities (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Références
  sales_rep_id UUID NOT NULL REFERENCES sales_representatives(id),
  lead_id UUID REFERENCES sales_leads(id),
  deal_id UUID REFERENCES sales_deals(id),

  -- Type d'activité
  activity_type VARCHAR(50) NOT NULL CHECK (activity_type IN (
    'call', 'email', 'meeting', 'demo', 'proposal', 'follow_up',
    'note', 'task', 'event', 'sms', 'whatsapp'
  )),

  -- Détails
  subject VARCHAR(255),
  description TEXT,
  duration_minutes INTEGER,

  -- Résultat
  outcome VARCHAR(50) CHECK (outcome IN (
    'successful', 'no_answer', 'voicemail', 'scheduled', 'not_interested',
    'needs_follow_up', 'closed_won', 'closed_lost'
  )),

  -- Analyse IA (si appel enregistré)
  sentiment_score DECIMAL(3, 2), -- -1 à +1
  key_points JSONB DEFAULT '[]',
  next_actions JSONB DEFAULT '[]',

  -- Enregistrement (si applicable)
  recording_url VARCHAR(500),
  transcript TEXT,

  -- Planning
  scheduled_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,

  -- Métadonnées
  metadata JSONB DEFAULT '{}',

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Créer la table des objectifs commerciaux (quotas)
CREATE TABLE IF NOT EXISTS sales_targets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Référence
  sales_rep_id UUID NOT NULL REFERENCES sales_representatives(id),

  -- Période
  period_type VARCHAR(20) CHECK (period_type IN ('daily', 'weekly', 'monthly', 'quarterly', 'yearly')),
  period_start DATE NOT NULL,
  period_end DATE NOT NULL,

  -- Objectifs
  target_deals INTEGER,
  target_revenue DECIMAL(12, 2),
  target_calls INTEGER,
  target_meetings INTEGER,

  -- Réalisations
  actual_deals INTEGER DEFAULT 0,
  actual_revenue DECIMAL(12, 2) DEFAULT 0,
  actual_calls INTEGER DEFAULT 0,
  actual_meetings INTEGER DEFAULT 0,

  -- Pourcentages
  deals_completion_pct DECIMAL(5, 2) DEFAULT 0,
  revenue_completion_pct DECIMAL(5, 2) DEFAULT 0,

  -- Récompenses
  bonus_eligible BOOLEAN DEFAULT false,
  bonus_amount DECIMAL(12, 2) DEFAULT 0,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. Créer la table des commissions (historique paiements)
CREATE TABLE IF NOT EXISTS sales_commissions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Référence
  sales_rep_id UUID NOT NULL REFERENCES sales_representatives(id),
  deal_id UUID REFERENCES sales_deals(id),

  -- Montants
  base_amount DECIMAL(12, 2) NOT NULL,
  bonus_amount DECIMAL(12, 2) DEFAULT 0,
  total_amount DECIMAL(12, 2) NOT NULL,

  -- Période
  period_start DATE,
  period_end DATE,

  -- Statut paiement
  status VARCHAR(50) DEFAULT 'pending' CHECK (status IN (
    'pending', 'processing', 'paid', 'held', 'cancelled'
  )),

  -- Paiement
  payment_method VARCHAR(50),
  payment_reference VARCHAR(255),
  paid_at TIMESTAMP WITH TIME ZONE,

  -- Détails
  notes TEXT,
  metadata JSONB DEFAULT '{}',

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- INDEXES pour performance
-- ============================================================================

-- Sales Representatives
CREATE INDEX IF NOT EXISTS idx_sales_reps_user_id ON sales_representatives(user_id);
CREATE INDEX IF NOT EXISTS idx_sales_reps_status ON sales_representatives(status);
CREATE INDEX IF NOT EXISTS idx_sales_reps_manager_id ON sales_representatives(manager_id);
CREATE INDEX IF NOT EXISTS idx_sales_reps_territory ON sales_representatives(territory);
CREATE INDEX IF NOT EXISTS idx_sales_reps_level_tier ON sales_representatives(level_tier);

-- Leads
CREATE INDEX IF NOT EXISTS idx_leads_sales_rep_id ON sales_leads(sales_rep_id);
CREATE INDEX IF NOT EXISTS idx_leads_status ON sales_leads(lead_status);
CREATE INDEX IF NOT EXISTS idx_leads_score ON sales_leads(score DESC);
CREATE INDEX IF NOT EXISTS idx_leads_next_followup ON sales_leads(next_follow_up_date);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON sales_leads(created_at DESC);

-- Deals
CREATE INDEX IF NOT EXISTS idx_deals_sales_rep_id ON sales_deals(sales_rep_id);
CREATE INDEX IF NOT EXISTS idx_deals_merchant_id ON sales_deals(merchant_id);
CREATE INDEX IF NOT EXISTS idx_deals_status ON sales_deals(status);
CREATE INDEX IF NOT EXISTS idx_deals_commission_status ON sales_deals(commission_status);
CREATE INDEX IF NOT EXISTS idx_deals_created_at ON sales_deals(created_at DESC);

-- Activities
CREATE INDEX IF NOT EXISTS idx_activities_sales_rep_id ON sales_activities(sales_rep_id);
CREATE INDEX IF NOT EXISTS idx_activities_lead_id ON sales_activities(lead_id);
CREATE INDEX IF NOT EXISTS idx_activities_type ON sales_activities(activity_type);
CREATE INDEX IF NOT EXISTS idx_activities_scheduled ON sales_activities(scheduled_at);

-- Targets
CREATE INDEX IF NOT EXISTS idx_targets_sales_rep_id ON sales_targets(sales_rep_id);
CREATE INDEX IF NOT EXISTS idx_targets_period ON sales_targets(period_start, period_end);

-- Commissions
CREATE INDEX IF NOT EXISTS idx_commissions_sales_rep_id ON sales_commissions(sales_rep_id);
CREATE INDEX IF NOT EXISTS idx_commissions_status ON sales_commissions(status);
CREATE INDEX IF NOT EXISTS idx_commissions_period ON sales_commissions(period_start, period_end);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Activer RLS sur toutes les tables
ALTER TABLE sales_representatives ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales_leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales_deals ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales_targets ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales_commissions ENABLE ROW LEVEL SECURITY;

-- Policies pour sales_representatives
CREATE POLICY "Sales reps can view own profile"
  ON sales_representatives FOR SELECT
  USING (auth.uid() = user_id OR auth.jwt()->>'role' = 'admin');

CREATE POLICY "Sales reps can update own profile"
  ON sales_representatives FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Admins have full access to sales reps"
  ON sales_representatives FOR ALL
  USING (auth.jwt()->>'role' = 'admin');

-- Policies pour sales_leads
CREATE POLICY "Sales reps view assigned leads"
  ON sales_leads FOR SELECT
  USING (
    sales_rep_id IN (
      SELECT id FROM sales_representatives WHERE user_id = auth.uid()
    )
    OR auth.jwt()->>'role' = 'admin'
  );

CREATE POLICY "Sales reps update assigned leads"
  ON sales_leads FOR UPDATE
  USING (
    sales_rep_id IN (
      SELECT id FROM sales_representatives WHERE user_id = auth.uid()
    )
  );

-- Policies pour sales_deals
CREATE POLICY "Sales reps view own deals"
  ON sales_deals FOR SELECT
  USING (
    sales_rep_id IN (
      SELECT id FROM sales_representatives WHERE user_id = auth.uid()
    )
    OR auth.jwt()->>'role' = 'admin'
  );

-- Policies pour sales_activities
CREATE POLICY "Sales reps manage own activities"
  ON sales_activities FOR ALL
  USING (
    sales_rep_id IN (
      SELECT id FROM sales_representatives WHERE user_id = auth.uid()
    )
  );

-- Policies pour sales_targets
CREATE POLICY "Sales reps view own targets"
  ON sales_targets FOR SELECT
  USING (
    sales_rep_id IN (
      SELECT id FROM sales_representatives WHERE user_id = auth.uid()
    )
    OR auth.jwt()->>'role' = 'admin'
  );

-- Policies pour sales_commissions
CREATE POLICY "Sales reps view own commissions"
  ON sales_commissions FOR SELECT
  USING (
    sales_rep_id IN (
      SELECT id FROM sales_representatives WHERE user_id = auth.uid()
    )
    OR auth.jwt()->>'role' = 'admin'
  );

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

-- Function pour mettre à jour updated_at automatiquement
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers pour updated_at
CREATE TRIGGER update_sales_reps_updated_at BEFORE UPDATE ON sales_representatives
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_leads_updated_at BEFORE UPDATE ON sales_leads
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_deals_updated_at BEFORE UPDATE ON sales_deals
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON sales_activities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_targets_updated_at BEFORE UPDATE ON sales_targets
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function pour calculer le score de lead automatiquement
CREATE OR REPLACE FUNCTION calculate_lead_score()
RETURNS TRIGGER AS $$
DECLARE
  score_value INTEGER := 0;
BEGIN
  -- Email fourni: +20 points
  IF NEW.contact_email IS NOT NULL AND NEW.contact_email != '' THEN
    score_value := score_value + 20;
  END IF;

  -- Téléphone fourni: +15 points
  IF NEW.contact_phone IS NOT NULL AND NEW.contact_phone != '' THEN
    score_value := score_value + 15;
  END IF;

  -- Entreprise de taille moyenne/grande: +25 points
  IF NEW.company_size IN ('51-200', '201-1000', '1000+') THEN
    score_value := score_value + 25;
  END IF;

  -- Budget estimé fourni: +20 points
  IF NEW.estimated_value IS NOT NULL AND NEW.estimated_value > 0 THEN
    score_value := score_value + 20;
  END IF;

  -- Lead source quality
  IF NEW.lead_source = 'referral' THEN
    score_value := score_value + 15;
  ELSIF NEW.lead_source = 'inbound' THEN
    score_value := score_value + 10;
  END IF;

  -- Status avancé: bonus
  IF NEW.lead_status IN ('qualified', 'proposal', 'negotiation') THEN
    score_value := score_value + 5;
  END IF;

  NEW.score := LEAST(score_value, 100);

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calculate_lead_score_trigger
  BEFORE INSERT OR UPDATE ON sales_leads
  FOR EACH ROW
  EXECUTE FUNCTION calculate_lead_score();

-- Function pour mettre à jour les stats du commercial
CREATE OR REPLACE FUNCTION update_sales_rep_stats()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' AND NEW.status = 'completed' THEN
    UPDATE sales_representatives
    SET
      total_deals = total_deals + 1,
      total_revenue = total_revenue + NEW.deal_value,
      commission_earned = commission_earned + NEW.commission_amount,
      updated_at = NOW()
    WHERE id = NEW.sales_rep_id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_rep_stats_on_deal
  AFTER INSERT OR UPDATE ON sales_deals
  FOR EACH ROW
  EXECUTE FUNCTION update_sales_rep_stats();

-- ============================================================================
-- DONNÉES INITIALES (Exemples)
-- ============================================================================

-- Insérer des niveaux de gamification par défaut
COMMENT ON COLUMN sales_representatives.level_tier IS
'Niveaux gamification: bronze(0-5K pts), silver(5K-15K), gold(15K-30K), platinum(30K-50K), diamond(50K+), legend(100K+)';

-- ============================================================================
-- VUES pour faciliter les requêtes
-- ============================================================================

-- Vue: Performance des commerciaux
CREATE OR REPLACE VIEW sales_rep_performance AS
SELECT
  sr.id,
  sr.first_name || ' ' || sr.last_name AS full_name,
  sr.territory,
  sr.level_tier,
  sr.total_deals,
  sr.total_revenue,
  sr.conversion_rate,
  sr.points,
  COUNT(DISTINCT sl.id) AS active_leads,
  COUNT(DISTINCT CASE WHEN sd.status = 'completed' THEN sd.id END) AS closed_deals_month,
  COALESCE(SUM(CASE WHEN sd.created_at >= DATE_TRUNC('month', CURRENT_DATE)
                    THEN sd.deal_value END), 0) AS revenue_this_month
FROM sales_representatives sr
LEFT JOIN sales_leads sl ON sl.sales_rep_id = sr.id AND sl.lead_status NOT IN ('closed_won', 'closed_lost')
LEFT JOIN sales_deals sd ON sd.sales_rep_id = sr.id
WHERE sr.status = 'active'
GROUP BY sr.id;

-- Vue: Pipeline de ventes
CREATE OR REPLACE VIEW sales_pipeline AS
SELECT
  lead_status,
  COUNT(*) AS lead_count,
  SUM(estimated_value) AS total_value,
  AVG(score) AS avg_score
FROM sales_leads
WHERE lead_status NOT IN ('closed_won', 'closed_lost')
GROUP BY lead_status;

-- ============================================================================
-- FIN DE LA MIGRATION
-- ============================================================================
