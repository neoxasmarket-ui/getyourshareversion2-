"""
Gamification Service - Système Complet
Pour Marchands, Influenceurs et Commerciaux
- Points & Niveaux
- Badges & Achievements
- Missions quotidiennes/hebdomadaires
- Leaderboards
- Récompenses
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
from decimal import Decimal

from utils.logger import logger


class UserType(str, Enum):
    """Types d'utilisateurs"""
    MERCHANT = "merchant"
    INFLUENCER = "influencer"
    SALES_REP = "commercial"


class LevelTier(str, Enum):
    """Niveaux de gamification"""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"
    LEGEND = "legend"


class GamificationService:
    """Service de gamification universel"""

    # Configuration des niveaux (points requis)
    LEVEL_THRESHOLDS = {
        LevelTier.BRONZE: 0,
        LevelTier.SILVER: 5000,
        LevelTier.GOLD: 15000,
        LevelTier.PLATINUM: 30000,
        LevelTier.DIAMOND: 50000,
        LevelTier.LEGEND: 100000
    }

    # Avantages par niveau
    LEVEL_BENEFITS = {
        LevelTier.BRONZE: {
            'commission_discount': 0,  # %
            'features': ['basic_analytics'],
            'support': 'email'
        },
        LevelTier.SILVER: {
            'commission_discount': 5,
            'features': ['basic_analytics', 'badge', 'priority_listing'],
            'support': 'email_priority'
        },
        LevelTier.GOLD: {
            'commission_discount': 10,
            'features': ['advanced_analytics', 'featured_products', 'ai_basic'],
            'support': 'chat'
        },
        LevelTier.PLATINUM: {
            'commission_discount': 15,
            'features': ['pro_analytics', 'dedicated_manager', 'ai_advanced'],
            'support': 'phone'
        },
        LevelTier.DIAMOND: {
            'commission_discount': 20,
            'features': ['all_features', 'custom_integrations', 'white_label'],
            'support': 'dedicated'
        },
        LevelTier.LEGEND: {
            'commission_discount': 25,
            'features': ['unlimited', 'revenue_share', 'partnership'],
            'support': 'vip'
        }
    }

    # Points par action
    POINTS_CONFIG = {
        UserType.MERCHANT: {
            'product_created': 10,
            'product_sold': 50,
            'first_sale': 500,
            'revenue_milestone_1000': 100,
            'revenue_milestone_10000': 500,
            'review_5_stars': 50,
            'quick_delivery': 25,
            'no_returns_month': 200,
            'referral_merchant': 300
        },
        UserType.INFLUENCER: {
            'post_created': 5,
            'sale_generated': 20,
            'first_sale': 200,
            'views_1000': 10,
            'views_10000': 50,
            'views_100000': 200,
            'engagement_high': 30,
            'collaboration_completed': 100,
            'viral_content': 500
        },
        UserType.SALES_REP: {
            'call_made': 5,
            'email_sent': 2,
            'meeting_scheduled': 15,
            'demo_completed': 20,
            'deal_closed': 100,
            'deal_large': 500,  # >50K MAD
            'target_achieved': 1000,
            'customer_referral': 200,
            'upsell_success': 150
        }
    }

    def __init__(self):
        self.db = None  # supabase client

    # ========================================
    # POINTS & NIVEAUX
    # ========================================

    async def award_points(
        self,
        user_id: str,
        user_type: UserType,
        action: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Attribuer des points pour une action

        Args:
            user_id: ID utilisateur
            user_type: Type (merchant, influencer, sales_rep)
            action: Action effectuée
            metadata: Métadonnées additionnelles

        Returns:
            Points attribués et nouveau total
        """
        # Calculer points basés sur l'action
        points = self._calculate_points(user_type, action, metadata)

        if points == 0:
            logger.warning(f"Action {action} non reconnue pour {user_type}")
            return {'points_awarded': 0, 'total_points': 0}

        # Récupérer points actuels
        current_points = await self._get_user_points(user_id, user_type)
        new_total = current_points + points

        # Mettre à jour dans DB
        await self._update_user_points(user_id, user_type, new_total)

        # Vérifier level up
        level_up_info = await self._check_level_up(user_id, user_type, current_points, new_total)

        # Logger l'événement
        await self._log_points_event(user_id, user_type, action, points, metadata)

        result = {
            'points_awarded': points,
            'total_points': new_total,
            'action': action,
            'level_up': level_up_info is not None,
            'level_info': level_up_info,
            'timestamp': datetime.now().isoformat()
        }

        logger.info(f"🎮 {points} points attribués à {user_id} pour {action}")

        return result

    def _calculate_points(
        self,
        user_type: UserType,
        action: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Calculer points pour une action"""
        config = self.POINTS_CONFIG.get(user_type, {})
        base_points = config.get(action, 0)

        # Multiplicateurs basés sur metadata
        if metadata:
            # Exemple: deal_value pour commerciaux
            if action == 'deal_closed' and 'deal_value' in metadata:
                deal_value = metadata['deal_value']
                if deal_value >= 50000:
                    base_points = config.get('deal_large', 500)

            # Exemple: nombre de vues pour influenceurs
            if 'views' in metadata:
                views = metadata['views']
                if views >= 100000:
                    base_points += config.get('views_100000', 200)
                elif views >= 10000:
                    base_points += config.get('views_10000', 50)
                elif views >= 1000:
                    base_points += config.get('views_1000', 10)

        return base_points

    async def _get_user_points(self, user_id: str, user_type: UserType) -> int:
        """Récupérer points actuels de l'utilisateur"""
        # En production: Query depuis la table appropriée
        # if user_type == UserType.MERCHANT:
        #     result = supabase.table('merchants').select('points').eq('user_id', user_id).single().execute()
        # elif user_type == UserType.INFLUENCER:
        #     result = supabase.table('influencers').select('points').eq('user_id', user_id).single().execute()
        # else:
        #     result = supabase.table('sales_representatives').select('points').eq('user_id', user_id).single().execute()
        #
        # return result.data.get('points', 0)

        return 0

    async def _update_user_points(self, user_id: str, user_type: UserType, new_total: int):
        """Mettre à jour points dans DB"""
        # En production: Update dans la table appropriée
        pass

    async def _check_level_up(
        self,
        user_id: str,
        user_type: UserType,
        old_points: int,
        new_points: int
    ) -> Optional[Dict[str, Any]]:
        """
        Vérifier si l'utilisateur monte de niveau

        Returns:
            Infos du level up si applicable, None sinon
        """
        old_tier = self._get_tier_from_points(old_points)
        new_tier = self._get_tier_from_points(new_points)

        if old_tier != new_tier:
            # Level up!
            benefits = self.LEVEL_BENEFITS[new_tier]

            # Mettre à jour tier dans DB
            await self._update_user_tier(user_id, user_type, new_tier)

            # Notification
            await self._send_level_up_notification(user_id, new_tier, benefits)

            logger.info(f"🎉 LEVEL UP! {user_id} → {new_tier.value.upper()}")

            return {
                'old_tier': old_tier.value,
                'new_tier': new_tier.value,
                'benefits': benefits,
                'congratulations_message': f"Félicitations! Vous êtes maintenant {new_tier.value.upper()}!"
            }

        return None

    def _get_tier_from_points(self, points: int) -> LevelTier:
        """Déterminer le tier basé sur points"""
        for tier in reversed(list(LevelTier)):
            if points >= self.LEVEL_THRESHOLDS[tier]:
                return tier
        return LevelTier.BRONZE

    async def _update_user_tier(self, user_id: str, user_type: UserType, new_tier: LevelTier):
        """Mettre à jour tier dans DB"""
        # En production: Update level_tier
        pass

    async def _send_level_up_notification(
        self,
        user_id: str,
        new_tier: LevelTier,
        benefits: Dict[str, Any]
    ):
        """Envoyer notification de level up"""
        # En production: Notification email/push
        pass

    async def _log_points_event(
        self,
        user_id: str,
        user_type: UserType,
        action: str,
        points: int,
        metadata: Optional[Dict[str, Any]]
    ):
        """Logger événement points dans historique"""
        event = {
            'user_id': user_id,
            'user_type': user_type.value,
            'action': action,
            'points': points,
            'metadata': metadata or {},
            'created_at': datetime.now()
        }

        # En production: Insert dans gamification_events table
        pass

    # ========================================
    # BADGES & ACHIEVEMENTS
    # ========================================

    # Définition des badges
    BADGES = {
        # Marchands
        'first_sale': {
            'name': 'Première Vente',
            'description': 'Réaliser votre première vente',
            'icon': '🎯',
            'user_types': [UserType.MERCHANT]
        },
        'speed_demon': {
            'name': 'Speed Demon',
            'description': '10 ventes en 24h',
            'icon': '⚡',
            'user_types': [UserType.MERCHANT]
        },
        'customer_favorite': {
            'name': 'Favori Client',
            'description': 'Note moyenne 4.8+',
            'icon': '⭐',
            'user_types': [UserType.MERCHANT]
        },
        'revenue_king': {
            'name': 'Roi du Revenu',
            'description': '100,000 MAD en un mois',
            'icon': '👑',
            'user_types': [UserType.MERCHANT]
        },

        # Influenceurs
        'viral_master': {
            'name': 'Viral Master',
            'description': 'Post avec 100K+ vues',
            'icon': '🔥',
            'user_types': [UserType.INFLUENCER]
        },
        'conversion_king': {
            'name': 'Roi Conversion',
            'description': 'Taux conversion >10%',
            'icon': '💎',
            'user_types': [UserType.INFLUENCER]
        },
        'consistent_creator': {
            'name': 'Créateur Régulier',
            'description': '30 jours consécutifs de posts',
            'icon': '📅',
            'user_types': [UserType.INFLUENCER]
        },

        # Commerciaux
        'closer': {
            'name': 'The Closer',
            'description': 'Taux de closing >50%',
            'icon': '🎯',
            'user_types': [UserType.SALES_REP]
        },
        'big_fish': {
            'name': 'Big Fish',
            'description': 'Deal >100,000 MAD',
            'icon': '🐋',
            'user_types': [UserType.SALES_REP]
        },
        'streak_master': {
            'name': 'Streak Master',
            'description': '10 jours consécutifs avec vente',
            'icon': '🔥',
            'user_types': [UserType.SALES_REP]
        }
    }

    async def award_badge(
        self,
        user_id: str,
        user_type: UserType,
        badge_key: str
    ) -> Dict[str, Any]:
        """
        Attribuer un badge à un utilisateur

        Args:
            user_id: ID utilisateur
            user_type: Type utilisateur
            badge_key: Clé du badge

        Returns:
            Badge attribué
        """
        badge_info = self.BADGES.get(badge_key)

        if not badge_info:
            logger.error(f"Badge {badge_key} inconnu")
            return {'error': 'Badge inconnu'}

        # Vérifier si badge applicable au type d'utilisateur
        if user_type not in badge_info['user_types']:
            return {'error': 'Badge non applicable'}

        # Vérifier si badge déjà obtenu
        has_badge = await self._user_has_badge(user_id, user_type, badge_key)
        if has_badge:
            return {'error': 'Badge déjà obtenu'}

        # Attribuer badge
        await self._add_badge_to_user(user_id, user_type, badge_key)

        # Bonus points pour le badge
        bonus_points = 100
        await self.award_points(user_id, user_type, f'badge_{badge_key}', {'badge': badge_key})

        # Notification
        await self._send_badge_notification(user_id, badge_info)

        logger.info(f"🏅 Badge {badge_key} attribué à {user_id}")

        return {
            'badge_key': badge_key,
            'badge_info': badge_info,
            'bonus_points': bonus_points,
            'timestamp': datetime.now().isoformat()
        }

    async def _user_has_badge(self, user_id: str, user_type: UserType, badge_key: str) -> bool:
        """Vérifier si utilisateur possède déjà le badge"""
        # En production: Query badges array
        return False

    async def _add_badge_to_user(self, user_id: str, user_type: UserType, badge_key: str):
        """Ajouter badge à l'utilisateur"""
        # En production: Update badges JSONB array
        pass

    async def _send_badge_notification(self, user_id: str, badge_info: Dict[str, Any]):
        """Envoyer notification de badge"""
        # En production: Email/push notification
        pass

    async def get_user_badges(self, user_id: str, user_type: UserType) -> List[Dict[str, Any]]:
        """Récupérer badges de l'utilisateur"""
        # En production: Query badges
        return []

    # ========================================
    # MISSIONS (Challenges Quotidiens/Hebdomadaires)
    # ========================================

    async def get_daily_missions(
        self,
        user_id: str,
        user_type: UserType
    ) -> List[Dict[str, Any]]:
        """
        Récupérer missions quotidiennes

        Returns:
            Liste des missions du jour avec progression
        """
        # Missions template par type
        missions_templates = {
            UserType.MERCHANT: [
                {
                    'id': 'add_3_products',
                    'title': 'Ajouter 3 nouveaux produits',
                    'description': 'Enrichissez votre catalogue',
                    'target': 3,
                    'reward_points': 50,
                    'reward_type': 'points'
                },
                {
                    'id': 'make_5_sales',
                    'title': 'Réaliser 5 ventes',
                    'description': 'Objectif ventes du jour',
                    'target': 5,
                    'reward_points': 100,
                    'reward_type': 'points'
                }
            ],
            UserType.INFLUENCER: [
                {
                    'id': 'create_content',
                    'title': 'Créer 1 contenu promotionnel',
                    'description': 'Publiez sur vos réseaux',
                    'target': 1,
                    'reward_points': 30,
                    'reward_type': 'points'
                },
                {
                    'id': 'generate_3_sales',
                    'title': 'Générer 3 ventes',
                    'description': 'Convertissez votre audience',
                    'target': 3,
                    'reward_points': 75,
                    'reward_type': 'points'
                }
            ],
            UserType.SALES_REP: [
                {
                    'id': 'make_20_calls',
                    'title': 'Passer 20 appels',
                    'description': 'Prospection active',
                    'target': 20,
                    'reward_points': 40,
                    'reward_type': 'points'
                },
                {
                    'id': 'close_2_deals',
                    'title': 'Fermer 2 deals',
                    'description': 'Objectif closing du jour',
                    'target': 2,
                    'reward_points': 150,
                    'reward_type': 'points'
                }
            ]
        }

        templates = missions_templates.get(user_type, [])

        # Récupérer progression réelle
        missions_with_progress = []
        for mission in templates:
            progress = await self._get_mission_progress(user_id, user_type, mission['id'])

            missions_with_progress.append({
                **mission,
                'current': progress,
                'completed': progress >= mission['target'],
                'completion_pct': min((progress / mission['target']) * 100, 100)
            })

        return missions_with_progress

    async def _get_mission_progress(
        self,
        user_id: str,
        user_type: UserType,
        mission_id: str
    ) -> int:
        """Récupérer progression d'une mission"""
        # En production: Query pour compter les actions du jour
        # Exemple: Compter produits créés aujourd'hui
        return 0

    async def complete_mission(
        self,
        user_id: str,
        user_type: UserType,
        mission_id: str
    ) -> Dict[str, Any]:
        """Marquer mission comme complétée et attribuer récompense"""
        # Vérifier si vraiment complétée
        missions = await self.get_daily_missions(user_id, user_type)
        mission = next((m for m in missions if m['id'] == mission_id), None)

        if not mission:
            return {'error': 'Mission introuvable'}

        if not mission['completed']:
            return {'error': 'Mission pas encore complétée'}

        # Vérifier si déjà réclamée
        claimed = await self._is_mission_claimed(user_id, mission_id)
        if claimed:
            return {'error': 'Récompense déjà réclamée'}

        # Attribuer récompense
        await self.award_points(
            user_id,
            user_type,
            f'mission_{mission_id}',
            {'mission': mission_id}
        )

        # Marquer comme réclamée
        await self._mark_mission_claimed(user_id, mission_id)

        logger.info(f"✅ Mission {mission_id} complétée par {user_id}")

        return {
            'mission_id': mission_id,
            'reward_points': mission['reward_points'],
            'timestamp': datetime.now().isoformat()
        }

    async def _is_mission_claimed(self, user_id: str, mission_id: str) -> bool:
        """Vérifier si mission déjà réclamée"""
        # En production: Query missions_completed table
        return False

    async def _mark_mission_claimed(self, user_id: str, mission_id: str):
        """Marquer mission comme réclamée"""
        # En production: Insert dans missions_completed
        pass

    # ========================================
    # LEADERBOARDS
    # ========================================

    async def get_leaderboard(
        self,
        user_type: UserType,
        period: str = 'month',  # week, month, all
        metric: str = 'points',  # points, revenue, deals
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Récupérer leaderboard

        Args:
            user_type: Type utilisateur
            period: Période (week, month, all)
            metric: Métrique de classement
            limit: Nombre de résultats

        Returns:
            Top performers
        """
        # En production: Query avec agrégations
        leaderboard = []

        return leaderboard

    async def get_user_rank(
        self,
        user_id: str,
        user_type: UserType,
        period: str = 'month'
    ) -> Dict[str, Any]:
        """Récupérer rang de l'utilisateur"""
        rank_info = {
            'user_id': user_id,
            'period': period,
            'rank': 0,
            'total_users': 0,
            'percentile': 0,
            'points_to_next_rank': 0
        }

        return rank_info


# Global instance
gamification_service = GamificationService()
