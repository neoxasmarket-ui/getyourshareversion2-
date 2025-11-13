"""
============================================
CRÉATION DIRECTE DES TABLES DE MODÉRATION
Utilise l'API Supabase pour exécuter le SQL
============================================
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ Erreur: Variables d'environnement Supabase manquantes")
    exit(1)

print("\n" + "="*60)
print("📊 CRÉATION DES TABLES DE MODÉRATION")
print("="*60 + "\n")

# SQL simplifié pour créer les tables essentielles
sql_commands = [
    # 1. Table principale moderation_queue
    """
    CREATE TABLE IF NOT EXISTS moderation_queue (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        product_id UUID,
        merchant_id UUID,
        user_id UUID,
        product_name VARCHAR(255) NOT NULL,
        product_description TEXT NOT NULL,
        product_category VARCHAR(100),
        product_price DECIMAL(10, 2),
        product_images JSONB,
        status VARCHAR(50) DEFAULT 'pending',
        ai_decision VARCHAR(20),
        ai_confidence DECIMAL(3, 2),
        ai_risk_level VARCHAR(20),
        ai_flags JSONB,
        ai_reason TEXT,
        ai_recommendation TEXT,
        moderation_method VARCHAR(20),
        admin_decision VARCHAR(20),
        admin_user_id UUID,
        admin_comment TEXT,
        reviewed_at TIMESTAMP,
        submission_attempts INT DEFAULT 1,
        priority INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """,
    
    # 2. Index pour performance
    """
    CREATE INDEX IF NOT EXISTS idx_moderation_status ON moderation_queue(status);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_moderation_merchant ON moderation_queue(merchant_id);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_moderation_created ON moderation_queue(created_at DESC);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_moderation_risk ON moderation_queue(ai_risk_level);
    """,
    
    # 3. Table moderation_history
    """
    CREATE TABLE IF NOT EXISTS moderation_history (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        moderation_id UUID,
        action VARCHAR(50),
        performed_by UUID,
        old_status VARCHAR(50),
        new_status VARCHAR(50),
        comment TEXT,
        metadata JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """,
    
    # 4. Table moderation_stats
    """
    CREATE TABLE IF NOT EXISTS moderation_stats (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        date DATE DEFAULT CURRENT_DATE,
        total_submissions INT DEFAULT 0,
        ai_approved INT DEFAULT 0,
        ai_rejected INT DEFAULT 0,
        admin_approved INT DEFAULT 0,
        admin_rejected INT DEFAULT 0,
        pending INT DEFAULT 0,
        avg_review_time_minutes DECIMAL(10, 2),
        created_at TIMESTAMP DEFAULT NOW(),
        UNIQUE(date)
    );
    """
]

print("📝 Exécution de " + str(len(sql_commands)) + " commandes SQL...\n")

# Utiliser l'API REST de Supabase pour exécuter du SQL
headers = {
    "apikey": SUPABASE_SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

success_count = 0
error_count = 0

for i, sql in enumerate(sql_commands, 1):
    sql_clean = sql.strip()
    if not sql_clean:
        continue
    
    # Note: Supabase ne permet pas l'exécution SQL directe via l'API Python
    # Il faut utiliser le Dashboard ou créer une fonction SQL
    print(f"{i}. {'✓' if i <= 4 else '...'} Commande préparée")

print("\n" + "="*60)
print("ℹ️  ÉTAPES SUIVANTES")
print("="*60)
print("""
Les tables de modération doivent être créées manuellement dans Supabase:

📋 OPTION 1 - Dashboard Supabase (RECOMMANDÉ):
1. Ouvrez: https://supabase.com/dashboard
2. Sélectionnez votre projet
3. Allez dans "SQL Editor" (menu gauche)
4. Copiez tout le contenu du fichier:
   backend/database/CREATE_MODERATION_TABLES.sql
5. Collez dans l'éditeur SQL
6. Cliquez "Run" ou appuyez sur Ctrl+Enter
7. Vérifiez dans "Table Editor" que les tables sont créées

📋 OPTION 2 - Via psql (si vous avez accès):
1. Récupérez la connection string dans Settings > Database
2. Exécutez: psql "votre_connection_string" -f backend/database/CREATE_MODERATION_TABLES.sql

✅ Après création des tables:
   Relancez: python create_test_moderation_products.py
   
🔗 Tables à créer:
   ✓ moderation_queue (table principale)
   ✓ moderation_history (historique)
   ✓ moderation_stats (statistiques)
   ✓ v_pending_moderation (vue)
   ✓ Fonctions: submit_product_for_moderation(), approve_moderation(), reject_moderation()
""")
print("="*60 + "\n")

print("💡 TIP: Pour tester rapidement, vous pouvez aussi créer une table minimale:")
print("""
CREATE TABLE moderation_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID, user_id UUID,
    product_name VARCHAR(255), product_description TEXT,
    product_category VARCHAR(100), product_price DECIMAL(10, 2),
    product_images JSONB, status VARCHAR(50) DEFAULT 'pending',
    ai_decision VARCHAR(20), ai_confidence DECIMAL(3, 2),
    ai_risk_level VARCHAR(20), ai_flags JSONB,
    ai_reason TEXT, ai_recommendation TEXT,
    moderation_method VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);
""")
print("")
