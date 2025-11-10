"""
Sales Representative Service
Gestion complète des commerciaux (Sales Reps)
- CRUD commerciaux
- Gestion leads & deals
- Scoring IA des leads
- Tracking activités
- Calcul commissions
- Gamification
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import random

from backend.utils.logger import logger


class SalesRepresentativeService:
    """Service de gestion des commerciaux"""

    def __init__(self):
        # En production, utiliser Supabase
        self.db = None  # supabase client

    # ========================================
    # GESTION COMMERCIAUX (CRUD)
    # ========================================

    async def create_sales_rep(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        territory: str = "Casablanca",
        manager_id: Optional[str] = None,
        commission_rate: float = 3.0
    ) -> Dict[str, Any]:
        """
        Créer un nouveau commercial

        Args:
            user_id: ID utilisateur
            first_name: Prénom
            last_name: Nom
            email: Email
            phone: Téléphone
            territory: Territoire (ville)
            manager_id: ID du manager (optionnel)
            commission_rate: Taux de commission %

        Returns:
            Profil commercial créé
        """
        employee_id = f"SR{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"

        sales_rep = {
            'user_id': user_id,
            'employee_id': employee_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'territory': territory,
            'manager_id': manager_id,
            'commission_rate': commission_rate,
            'status': 'active',
            'level': 'junior',
            'level_tier': 'bronze',
            'points': 0,
            'total_deals': 0,
            'total_revenue': Decimal('0.00'),
            'commission_earned': Decimal('0.00'),
            'hire_date': datetime.now().date(),
            'created_at': datetime.now()
        }

        # En production: Insert dans Supabase
        # result = supabase.table('sales_representatives').insert(sales_rep).execute()

        logger.info(f"✅ Commercial créé: {first_name} {last_name} ({employee_id})")

        return sales_rep

    async def get_sales_rep(self, sales_rep_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer profil commercial"""
        # En production: Query Supabase
        # result = supabase.table('sales_representatives').select('*').eq('id', sales_rep_id).execute()

        return None

    async def update_sales_rep(
        self,
        sales_rep_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Mettre à jour profil commercial"""
        updates['updated_at'] = datetime.now()

        # En production: Update Supabase
        # result = supabase.table('sales_representatives').update(updates).eq('id', sales_rep_id).execute()

        logger.info(f"✅ Commercial mis à jour: {sales_rep_id}")

        return updates

    async def get_team_members(self, manager_id: str) -> List[Dict[str, Any]]:
        """Récupérer l'équipe d'un manager"""
        # En production: Query team
        # result = supabase.table('sales_representatives').select('*').eq('manager_id', manager_id).execute()

        return []

    # ========================================
    # GESTION LEADS (Prospects)
    # ========================================

    async def create_lead(
        self,
        sales_rep_id: str,
        contact_name: str,
        contact_email: str,
        contact_phone: str,
        company_name: Optional[str] = None,
        estimated_value: Optional[float] = None,
        product_interest: Optional[str] = None,
        lead_source: str = 'inbound',
        **kwargs
    ) -> Dict[str, Any]:
        """
        Créer un nouveau lead (prospect)

        Args:
            sales_rep_id: ID commercial assigné
            contact_name: Nom du contact
            contact_email: Email
            contact_phone: Téléphone
            company_name: Nom entreprise
            estimated_value: Valeur estimée du deal
            product_interest: Produit d'intérêt
            lead_source: Source ('inbound', 'outbound', 'referral')

        Returns:
            Lead créé avec score IA
        """
        lead = {
            'sales_rep_id': sales_rep_id,
            'contact_name': contact_name,
            'contact_email': contact_email,
            'contact_phone': contact_phone,
            'company_name': company_name,
            'estimated_value': Decimal(str(estimated_value)) if estimated_value else None,
            'product_interest': product_interest,
            'lead_source': lead_source,
            'lead_status': 'new',
            'assigned_at': datetime.now(),
            'created_at': datetime.now(),
            **kwargs
        }

        # Calculer score IA automatiquement (trigger SQL le fera aussi)
        lead['score'] = await self._calculate_lead_score(lead)
        lead['probability_to_close'] = self._calculate_probability(lead['score'])

        # En production: Insert Supabase
        # result = supabase.table('sales_leads').insert(lead).execute()

        logger.info(f"✅ Lead créé: {contact_name} (Score: {lead['score']}/100)")

        return lead

    async def _calculate_lead_score(self, lead: Dict[str, Any]) -> int:
        """
        Calculer score IA du lead (0-100)

        Facteurs:
        - Email fourni: +20
        - Téléphone fourni: +15
        - Entreprise (B2B): +25
        - Budget estimé: +20
        - Source qualité: +15
        - Position senior: +5
        """
        score = 0

        # Email
        if lead.get('contact_email'):
            score += 20

        # Téléphone
        if lead.get('contact_phone'):
            score += 15

        # Entreprise B2B
        if lead.get('company_name'):
            score += 25

        # Budget estimé
        if lead.get('estimated_value') and lead['estimated_value'] > 0:
            score += 20

        # Source
        if lead.get('lead_source') == 'referral':
            score += 15
        elif lead.get('lead_source') == 'inbound':
            score += 10

        # Position senior
        if lead.get('position'):
            senior_positions = ['ceo', 'cto', 'director', 'manager', 'founder', 'owner']
            if any(pos in lead['position'].lower() for pos in senior_positions):
                score += 5

        return min(score, 100)

    def _calculate_probability(self, score: int) -> float:
        """Calculer probabilité de conversion basée sur score"""
        # Formule simple: score * 0.7 pour avoir une probabilité plus réaliste
        return round(score * 0.7, 2)

    async def update_lead_status(
        self,
        lead_id: str,
        new_status: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Mettre à jour statut du lead

        Statuts: new, contacted, qualified, proposal, negotiation,
                 closed_won, closed_lost, on_hold, nurturing
        """
        updates = {
            'lead_status': new_status,
            'updated_at': datetime.now()
        }

        if notes:
            updates['notes'] = notes

        # Si fermé (won ou lost)
        if new_status in ['closed_won', 'closed_lost']:
            updates['closed_at'] = datetime.now()

        # En production: Update Supabase
        # result = supabase.table('sales_leads').update(updates).eq('id', lead_id).execute()

        logger.info(f"✅ Lead {lead_id} → {new_status}")

        return updates

    async def get_leads_by_sales_rep(
        self,
        sales_rep_id: str,
        status: Optional[str] = None,
        sort_by: str = 'score',  # score, created_at, estimated_value
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Récupérer leads d'un commercial"""
        # En production: Query with filters
        # query = supabase.table('sales_leads').select('*').eq('sales_rep_id', sales_rep_id)
        #
        # if status:
        #     query = query.eq('lead_status', status)
        #
        # if sort_by == 'score':
        #     query = query.order('score', desc=True)
        # elif sort_by == 'estimated_value':
        #     query = query.order('estimated_value', desc=True)
        # else:
        #     query = query.order('created_at', desc=True)
        #
        # result = query.limit(limit).execute()

        return []

    async def get_hot_leads(
        self,
        sales_rep_id: str,
        min_score: int = 70
    ) -> List[Dict[str, Any]]:
        """
        Récupérer leads HOT (haute probabilité)

        Leads avec score >= 70 et follow-up aujourd'hui
        """
        # En production: Query avec score élevé
        # result = supabase.table('sales_leads')\
        #     .select('*')\
        #     .eq('sales_rep_id', sales_rep_id)\
        #     .gte('score', min_score)\
        #     .or_('next_follow_up_date.lte.{}'.format(datetime.now().date()))\
        #     .order('score', desc=True)\
        #     .execute()

        return []

    # ========================================
    # GESTION DEALS (Ventes fermées)
    # ========================================

    async def create_deal(
        self,
        sales_rep_id: str,
        lead_id: str,
        deal_name: str,
        deal_value: float,
        deal_type: str = 'service_fixed',  # product_commission, service_fixed
        commission_rate: Optional[float] = None,
        merchant_id: Optional[str] = None,
        service_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Créer un deal (vente fermée)

        Args:
            sales_rep_id: ID commercial
            lead_id: ID du lead
            deal_name: Nom du deal
            deal_value: Valeur totale
            deal_type: Type (product_commission, service_fixed)
            commission_rate: Taux commission (% ou fixe)
            merchant_id: ID marchand si vente produit
            service_name: Nom service si vente service

        Returns:
            Deal créé
        """
        # Récupérer taux commission du commercial si non fourni
        if commission_rate is None:
            sales_rep = await self.get_sales_rep(sales_rep_id)
            commission_rate = sales_rep.get('commission_rate', 3.0) if sales_rep else 3.0

        # Calculer commission
        if deal_type == 'product_commission':
            # Commission en %
            commission_amount = Decimal(str(deal_value)) * (Decimal(str(commission_rate)) / 100)
        else:
            # Commission fixe par deal
            commission_amount = Decimal(str(commission_rate))

        deal = {
            'sales_rep_id': sales_rep_id,
            'lead_id': lead_id,
            'merchant_id': merchant_id,
            'deal_name': deal_name,
            'deal_type': deal_type,
            'deal_value': Decimal(str(deal_value)),
            'commission_rate': Decimal(str(commission_rate)),
            'commission_amount': commission_amount,
            'service_name': service_name,
            'status': 'pending',
            'commission_status': 'pending',
            'created_at': datetime.now(),
            **kwargs
        }

        # En production: Insert Supabase
        # result = supabase.table('sales_deals').insert(deal).execute()

        # Mettre à jour le lead en closed_won
        await self.update_lead_status(lead_id, 'closed_won', f'Deal créé: {deal_name}')

        # Ajouter points gamification
        await self._award_points(sales_rep_id, 'deal_closed', deal_value)

        logger.info(f"✅ Deal créé: {deal_name} - {deal_value} MAD (Commission: {commission_amount} MAD)")

        return deal

    async def get_deals_by_sales_rep(
        self,
        sales_rep_id: str,
        status: Optional[str] = None,
        period: str = 'all'  # all, today, week, month, year
    ) -> List[Dict[str, Any]]:
        """Récupérer deals d'un commercial"""
        # En production: Query with filters
        # query = supabase.table('sales_deals').select('*').eq('sales_rep_id', sales_rep_id)
        #
        # if status:
        #     query = query.eq('status', status)
        #
        # if period == 'today':
        #     query = query.gte('created_at', datetime.now().date())
        # elif period == 'week':
        #     week_ago = datetime.now() - timedelta(days=7)
        #     query = query.gte('created_at', week_ago)
        # elif period == 'month':
        #     month_start = datetime.now().replace(day=1)
        #     query = query.gte('created_at', month_start)
        #
        # result = query.order('created_at', desc=True).execute()

        return []

    async def approve_commission(
        self,
        deal_id: str,
        payment_reference: Optional[str] = None
    ) -> Dict[str, Any]:
        """Approuver et payer commission"""
        updates = {
            'commission_status': 'paid',
            'paid_at': datetime.now(),
            'payment_reference': payment_reference,
            'updated_at': datetime.now()
        }

        # En production: Update Supabase
        # result = supabase.table('sales_deals').update(updates).eq('id', deal_id).execute()

        logger.info(f"✅ Commission approuvée pour deal: {deal_id}")

        return updates

    # ========================================
    # ACTIVITÉS (Appels, Emails, Réunions)
    # ========================================

    async def log_activity(
        self,
        sales_rep_id: str,
        activity_type: str,  # call, email, meeting, demo
        lead_id: Optional[str] = None,
        subject: Optional[str] = None,
        description: Optional[str] = None,
        duration_minutes: Optional[int] = None,
        outcome: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Logger une activité commerciale

        Types: call, email, meeting, demo, proposal, follow_up, note
        """
        activity = {
            'sales_rep_id': sales_rep_id,
            'lead_id': lead_id,
            'activity_type': activity_type,
            'subject': subject,
            'description': description,
            'duration_minutes': duration_minutes,
            'outcome': outcome,
            'completed_at': datetime.now(),
            'created_at': datetime.now(),
            **kwargs
        }

        # En production: Insert Supabase
        # result = supabase.table('sales_activities').insert(activity).execute()

        # Mettre à jour compteur de contact du lead
        if lead_id:
            # Incrémenter contact_count
            pass

        # Gamification: points pour activité
        points_map = {
            'call': 5,
            'email': 2,
            'meeting': 15,
            'demo': 20,
            'proposal': 25
        }
        if activity_type in points_map:
            await self._award_points(sales_rep_id, f'activity_{activity_type}', points_map[activity_type])

        logger.info(f"✅ Activité loggée: {activity_type} - {subject}")

        return activity

    async def get_activities(
        self,
        sales_rep_id: str,
        lead_id: Optional[str] = None,
        activity_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Récupérer activités"""
        # En production: Query with filters
        return []

    # ========================================
    # DASHBOARD & ANALYTICS
    # ========================================

    async def get_dashboard_stats(self, sales_rep_id: str) -> Dict[str, Any]:
        """
        Récupérer stats pour dashboard commercial

        Returns:
            KPIs et métriques clés
        """
        # En production: Queries complexes

        # Deals ce mois
        month_start = datetime.now().replace(day=1)

        stats = {
            'overview': {
                'total_deals': 0,  # Tous les deals
                'total_revenue': 0,  # Revenu total généré
                'commission_earned': 0,  # Commission gagnée
                'commission_pending': 0,  # Commission en attente
                'conversion_rate': 0,  # %
                'rank': 0  # Classement dans l'équipe
            },

            'this_month': {
                'deals': 0,
                'revenue': 0,
                'calls': 0,
                'meetings': 0,
                'target_completion': 0  # % objectif atteint
            },

            'today': {
                'calls_scheduled': 0,
                'meetings_scheduled': 0,
                'tasks_pending': 0,
                'hot_leads': 0  # Leads score >70
            },

            'pipeline': {
                'new': 0,
                'contacted': 0,
                'qualified': 0,
                'proposal': 0,
                'negotiation': 0,
                'total_value': 0
            },

            'gamification': {
                'points': 0,
                'level_tier': 'bronze',
                'badges': [],
                'achievements': [],
                'rank_global': 0,
                'next_level_points': 5000
            },

            'leaderboard': {
                'position': 0,
                'top_performers': []  # Top 5
            },

            'recommendations': []  # Recommandations IA
        }

        return stats

    async def get_performance_metrics(
        self,
        sales_rep_id: str,
        period: str = 'month'  # week, month, quarter, year
    ) -> Dict[str, Any]:
        """Métriques de performance détaillées"""
        metrics = {
            'period': period,
            'deals': {
                'total': 0,
                'won': 0,
                'lost': 0,
                'win_rate': 0
            },
            'revenue': {
                'total': 0,
                'average_deal_size': 0,
                'largest_deal': 0
            },
            'activity': {
                'calls': 0,
                'emails': 0,
                'meetings': 0,
                'demos': 0
            },
            'leads': {
                'new': 0,
                'converted': 0,
                'conversion_rate': 0
            },
            'targets': {
                'deals_target': 0,
                'deals_actual': 0,
                'revenue_target': 0,
                'revenue_actual': 0
            }
        }

        return metrics

    # ========================================
    # GAMIFICATION
    # ========================================

    async def _award_points(
        self,
        sales_rep_id: str,
        action: str,
        value: float = 0
    ) -> int:
        """
        Attribuer points gamification

        Actions:
        - deal_closed: points basés sur valeur deal
        - activity_call: 5 points
        - activity_meeting: 15 points
        - etc.
        """
        points = 0

        if action == 'deal_closed':
            # 1 point par 100 MAD
            points = int(value / 100)
        elif action.startswith('activity_'):
            points = int(value)
        else:
            points = 10  # Default

        # Mettre à jour points total
        # En production: Update sales_representatives
        # supabase.table('sales_representatives')\
        #     .update({'points': sales_representatives.points + points})\
        #     .eq('id', sales_rep_id)\
        #     .execute()

        # Vérifier si nouveau level atteint
        await self._check_level_up(sales_rep_id)

        logger.info(f"🎮 Points attribués: {points} pour {action}")

        return points

    async def _check_level_up(self, sales_rep_id: str):
        """Vérifier et mettre à jour le niveau gamification"""
        # Récupérer points actuels
        sales_rep = await self.get_sales_rep(sales_rep_id)
        if not sales_rep:
            return

        points = sales_rep.get('points', 0)
        current_tier = sales_rep.get('level_tier', 'bronze')

        # Niveaux
        tiers = {
            'bronze': 0,
            'silver': 5000,
            'gold': 15000,
            'platinum': 30000,
            'diamond': 50000,
            'legend': 100000
        }

        # Trouver nouveau tier
        new_tier = 'bronze'
        for tier, min_points in sorted(tiers.items(), key=lambda x: x[1], reverse=True):
            if points >= min_points:
                new_tier = tier
                break

        # Si level up
        if new_tier != current_tier:
            await self.update_sales_rep(sales_rep_id, {'level_tier': new_tier})
            logger.info(f"🎉 LEVEL UP! {sales_rep['first_name']} → {new_tier.upper()}")

            # Notification au commercial
            # Envoyer email/notification

    async def get_leaderboard(
        self,
        period: str = 'month',  # week, month, all
        territory: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Récupérer leaderboard des commerciaux

        Classement par:
        - Deals fermés
        - Revenu généré
        - Points gamification
        """
        # En production: Query avec agrégations
        leaderboard = []

        return leaderboard

    # ========================================
    # COMMISSIONS & PAIEMENTS
    # ========================================

    async def calculate_monthly_commission(
        self,
        sales_rep_id: str,
        month: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Calculer commission mensuelle

        Returns:
            Détails de la commission
        """
        if month is None:
            month = datetime.now().replace(day=1)

        month_end = (month.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        # Récupérer tous les deals du mois avec status completed
        # deals = await self.get_deals_by_sales_rep(
        #     sales_rep_id,
        #     status='completed',
        #     period='custom'  # month_start à month_end
        # )

        base_commission = Decimal('0.00')
        bonus = Decimal('0.00')
        total_commission = Decimal('0.00')

        commission_record = {
            'sales_rep_id': sales_rep_id,
            'period_start': month,
            'period_end': month_end,
            'base_amount': base_commission,
            'bonus_amount': bonus,
            'total_amount': total_commission,
            'status': 'pending',
            'created_at': datetime.now()
        }

        # En production: Insert dans sales_commissions
        # result = supabase.table('sales_commissions').insert(commission_record).execute()

        return commission_record

    # ========================================
    # OBJECTIFS (Targets/Quotas)
    # ========================================

    async def set_target(
        self,
        sales_rep_id: str,
        period_type: str,  # daily, weekly, monthly, quarterly
        period_start: datetime,
        period_end: datetime,
        target_deals: Optional[int] = None,
        target_revenue: Optional[float] = None,
        target_calls: Optional[int] = None
    ) -> Dict[str, Any]:
        """Définir objectif pour un commercial"""
        target = {
            'sales_rep_id': sales_rep_id,
            'period_type': period_type,
            'period_start': period_start,
            'period_end': period_end,
            'target_deals': target_deals,
            'target_revenue': Decimal(str(target_revenue)) if target_revenue else None,
            'target_calls': target_calls,
            'actual_deals': 0,
            'actual_revenue': Decimal('0.00'),
            'actual_calls': 0,
            'created_at': datetime.now()
        }

        # En production: Insert Supabase
        # result = supabase.table('sales_targets').insert(target).execute()

        logger.info(f"🎯 Objectif défini: {target_deals} deals, {target_revenue} MAD")

        return target

    async def get_target_progress(
        self,
        sales_rep_id: str,
        period_type: str = 'monthly'
    ) -> Dict[str, Any]:
        """Récupérer progression vers objectifs"""
        # En production: Query current target
        progress = {
            'period_type': period_type,
            'targets': {
                'deals': 0,
                'revenue': 0,
                'calls': 0
            },
            'actual': {
                'deals': 0,
                'revenue': 0,
                'calls': 0
            },
            'completion': {
                'deals_pct': 0,
                'revenue_pct': 0,
                'calls_pct': 0
            },
            'on_track': False,
            'days_remaining': 0
        }

        return progress


# Global instance
sales_rep_service = SalesRepresentativeService()


# FastAPI endpoints example
if __name__ == "__main__":
    """
    from fastapi import APIRouter, Depends

    router = APIRouter(prefix="/api/sales")

    @router.post("/leads")
    async def create_lead(lead_data: dict):
        return await sales_rep_service.create_lead(**lead_data)

    @router.get("/dashboard/{sales_rep_id}")
    async def get_dashboard(sales_rep_id: str):
        return await sales_rep_service.get_dashboard_stats(sales_rep_id)

    @router.get("/leaderboard")
    async def get_leaderboard(period: str = 'month'):
        return await sales_rep_service.get_leaderboard(period=period)
    """
    pass
