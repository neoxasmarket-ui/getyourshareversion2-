"""
Advanced Analytics Service avec IA
Analytics Pro pour Marchands, Influenceurs et Commerciaux
- Insights détaillés avec IA
- Recommandations personnalisées
- Prédictions & forecasting
- Anomaly detection
- Comparative analytics
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import statistics

from utils.logger import logger


class AdvancedAnalyticsService:
    """Service d'analytics avancés avec IA"""

    def __init__(self):
        self.db = None  # supabase client

    # ========================================
    # MARCHANDS ANALYTICS
    # ========================================

    async def get_merchant_analytics(
        self,
        merchant_id: str,
        period: str = 'month',  # week, month, quarter, year
        compare_previous: bool = True
    ) -> Dict[str, Any]:
        """
        Analytics complets pour marchands

        Returns:
            Métriques + insights IA + recommandations
        """
        # Période actuelle et précédente
        current_period = self._get_period_dates(period)
        previous_period = self._get_previous_period_dates(period)

        # Métriques principales
        metrics = await self._get_merchant_metrics(merchant_id, current_period)
        previous_metrics = await self._get_merchant_metrics(merchant_id, previous_period) if compare_previous else None

        # Calculer tendances
        trends = self._calculate_trends(metrics, previous_metrics) if previous_metrics else {}

        # Insights IA
        insights = await self._generate_merchant_insights(merchant_id, metrics, trends)

        # Recommandations
        recommendations = await self._generate_merchant_recommendations(merchant_id, metrics, insights)

        # Prédictions
        predictions = await self._generate_merchant_predictions(merchant_id, metrics)

        # Top produits
        top_products = await self._get_top_products(merchant_id, current_period, limit=5)

        # Performance par catégorie
        category_performance = await self._get_category_performance(merchant_id, current_period)

        return {
            'period': period,
            'date_range': {
                'start': current_period['start'],
                'end': current_period['end']
            },
            'metrics': {
                'current': metrics,
                'previous': previous_metrics,
                'trends': trends
            },
            'insights': insights,
            'recommendations': recommendations,
            'predictions': predictions,
            'top_products': top_products,
            'category_performance': category_performance,
            'generated_at': datetime.now().isoformat()
        }

    async def _get_merchant_metrics(
        self,
        merchant_id: str,
        period: Dict[str, datetime]
    ) -> Dict[str, Any]:
        """Récupérer métriques marchand pour une période"""
        # En production: Complex queries

        metrics = {
            'revenue': {
                'total': 0,
                'by_day': [],  # Série temporelle
                'average_per_day': 0
            },
            'sales': {
                'total_orders': 0,
                'completed_orders': 0,
                'cancelled_orders': 0,
                'average_order_value': 0,
                'by_day': []
            },
            'products': {
                'total_active': 0,
                'new_added': 0,
                'out_of_stock': 0,
                'low_stock': 0
            },
            'customers': {
                'total': 0,
                'new': 0,
                'returning': 0,
                'retention_rate': 0
            },
            'traffic': {
                'total_views': 0,
                'unique_visitors': 0,
                'conversion_rate': 0,
                'bounce_rate': 0
            },
            'reviews': {
                'average_rating': 0,
                'total_reviews': 0,
                'positive': 0,
                'negative': 0
            }
        }

        return metrics

    def _calculate_trends(
        self,
        current: Dict[str, Any],
        previous: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculer tendances (% changement)"""
        trends = {}

        # Revenue trend
        current_revenue = current['revenue']['total']
        previous_revenue = previous['revenue']['total']
        if previous_revenue > 0:
            trends['revenue'] = ((current_revenue - previous_revenue) / previous_revenue) * 100
        else:
            trends['revenue'] = 100 if current_revenue > 0 else 0

        # Orders trend
        current_orders = current['sales']['total_orders']
        previous_orders = previous['sales']['total_orders']
        if previous_orders > 0:
            trends['orders'] = ((current_orders - previous_orders) / previous_orders) * 100
        else:
            trends['orders'] = 100 if current_orders > 0 else 0

        # Conversion rate trend
        current_conv = current['traffic']['conversion_rate']
        previous_conv = previous['traffic']['conversion_rate']
        if previous_conv > 0:
            trends['conversion_rate'] = ((current_conv - previous_conv) / previous_conv) * 100
        else:
            trends['conversion_rate'] = 100 if current_conv > 0 else 0

        return trends

    async def _generate_merchant_insights(
        self,
        merchant_id: str,
        metrics: Dict[str, Any],
        trends: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """
        Générer insights IA pour marchands

        Types d'insights:
        - Performance alerts
        - Opportunities detected
        - Anomalies
        - Achievements
        """
        insights = []

        # Insight: Strong growth
        if trends.get('revenue', 0) > 20:
            insights.append({
                'type': 'positive',
                'category': 'growth',
                'title': 'Forte croissance détectée',
                'message': f"Votre revenu a augmenté de {trends['revenue']:.1f}% ce mois!",
                'impact': 'high',
                'action': 'Continuez sur cette lancée en ajoutant plus de produits similaires'
            })

        # Insight: Declining performance
        if trends.get('orders', 0) < -15:
            insights.append({
                'type': 'warning',
                'category': 'decline',
                'title': 'Baisse des commandes',
                'message': f"Vos commandes ont baissé de {abs(trends['orders']):.1f}%",
                'impact': 'high',
                'action': 'Lancez une promotion ou contactez vos clients inactifs'
            })

        # Insight: Low stock
        low_stock = metrics['products']['low_stock']
        if low_stock > 0:
            insights.append({
                'type': 'warning',
                'category': 'inventory',
                'title': 'Stock faible détecté',
                'message': f"{low_stock} produit(s) en rupture imminente",
                'impact': 'medium',
                'action': 'Réapprovisionnez rapidement pour éviter les ventes manquées'
            })

        # Insight: High conversion rate
        if metrics['traffic']['conversion_rate'] > 5:
            insights.append({
                'type': 'positive',
                'category': 'performance',
                'title': 'Excellent taux de conversion',
                'message': f"{metrics['traffic']['conversion_rate']:.1f}% de conversion",
                'impact': 'medium',
                'action': 'Augmentez votre trafic pour maximiser les ventes'
            })

        # Insight: Customer retention
        retention = metrics['customers']['retention_rate']
        if retention < 30:
            insights.append({
                'type': 'info',
                'category': 'retention',
                'title': 'Rétention à améliorer',
                'message': f"Seulement {retention:.0f}% de clients fidèles",
                'impact': 'medium',
                'action': 'Créez un programme de fidélité ou offrez des coupons'
            })

        return insights

    async def _generate_merchant_recommendations(
        self,
        merchant_id: str,
        metrics: Dict[str, Any],
        insights: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Générer recommandations personnalisées IA

        Returns:
            Top 5 recommendations prioritisées
        """
        recommendations = []

        # Reco: Optimize pricing
        if metrics['sales']['average_order_value'] < 300:
            recommendations.append({
                'priority': 'high',
                'category': 'pricing',
                'title': 'Augmentez votre panier moyen',
                'description': 'Votre AOV est de {metrics["sales"]["average_order_value"]} MAD',
                'actions': [
                    'Créez des bundles de produits',
                    'Offrez la livraison gratuite au-dessus de 500 MAD',
                    'Proposez des upsells au checkout'
                ],
                'estimated_impact': '+25% revenu'
            })

        # Reco: Add more products
        if metrics['products']['total_active'] < 10:
            recommendations.append({
                'priority': 'medium',
                'category': 'catalog',
                'title': 'Élargissez votre catalogue',
                'description': f"Vous n'avez que {metrics['products']['total_active']} produits actifs",
                'actions': [
                    'Ajoutez au moins 10 produits supplémentaires',
                    'Diversifiez vos catégories',
                    'Utilisez l\'IA pour générer descriptions'
                ],
                'estimated_impact': '+40% ventes'
            })

        # Reco: Improve reviews
        if metrics['reviews']['average_rating'] < 4.5:
            recommendations.append({
                'priority': 'high',
                'category': 'reputation',
                'title': 'Améliorez vos notes',
                'description': f"Note moyenne: {metrics['reviews']['average_rating']}/5",
                'actions': [
                    'Demandez des avis à vos clients satisfaits',
                    'Résolvez les problèmes des clients insatisfaits',
                    'Offrez un service client exceptionnel'
                ],
                'estimated_impact': '+15% conversions'
            })

        # Reco: Influencer collaboration
        recommendations.append({
            'priority': 'medium',
            'category': 'marketing',
            'title': 'Collaborez avec des influenceurs',
            'description': 'Boostez votre visibilité',
            'actions': [
                'Trouvez des influenceurs via notre matching',
                'Lancez une campagne test avec 2-3 influenceurs',
                'Mesurez le ROI et scalez'
            ],
            'estimated_impact': '+60% reach'
        })

        # Trier par priorité
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recommendations.sort(key=lambda x: priority_order[x['priority']])

        return recommendations[:5]

    async def _generate_merchant_predictions(
        self,
        merchant_id: str,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prédictions ML pour marchands

        Returns:
            Prédictions revenus, ventes, croissance
        """
        # Simplified predictions (en production: vrai ML model)

        current_revenue = metrics['revenue']['total']
        current_orders = metrics['sales']['total_orders']

        # Prédiction simple basée sur moyenne
        predictions = {
            'next_month': {
                'revenue': {
                    'min': current_revenue * 0.9,
                    'expected': current_revenue * 1.1,
                    'max': current_revenue * 1.3,
                    'confidence': 75
                },
                'orders': {
                    'min': int(current_orders * 0.9),
                    'expected': int(current_orders * 1.1),
                    'max': int(current_orders * 1.3),
                    'confidence': 75
                }
            },
            'next_quarter': {
                'revenue': {
                    'min': current_revenue * 2.7,
                    'expected': current_revenue * 3.3,
                    'max': current_revenue * 4.0,
                    'confidence': 60
                }
            },
            'seasonal_trends': {
                'best_month': 'Décembre',
                'worst_month': 'Août',
                'upcoming_peak': 'Black Friday (25 Nov)'
            }
        }

        return predictions

    async def _get_top_products(
        self,
        merchant_id: str,
        period: Dict[str, datetime],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Top produits par ventes"""
        # En production: Query avec ORDER BY
        return []

    async def _get_category_performance(
        self,
        merchant_id: str,
        period: Dict[str, datetime]
    ) -> List[Dict[str, Any]]:
        """Performance par catégorie"""
        return []

    # ========================================
    # INFLUENCEURS ANALYTICS
    # ========================================

    async def get_influencer_analytics(
        self,
        influencer_id: str,
        period: str = 'month'
    ) -> Dict[str, Any]:
        """
        Analytics complets pour influenceurs

        Returns:
            Métriques + insights + recommandations
        """
        current_period = self._get_period_dates(period)

        # Métriques
        metrics = {
            'content': {
                'total_posts': 0,
                'total_views': 0,
                'total_engagement': 0,
                'avg_engagement_rate': 0,
                'viral_posts': 0  # >100K views
            },
            'sales': {
                'total_sales_generated': 0,
                'total_revenue_generated': 0,
                'conversion_rate': 0,
                'average_commission': 0
            },
            'audience': {
                'followers_start': 0,
                'followers_end': 0,
                'followers_growth': 0,
                'followers_growth_rate': 0
            },
            'campaigns': {
                'total_active': 0,
                'total_completed': 0,
                'average_roi': 0,
                'best_performing_category': ''
            }
        }

        # Insights IA
        insights = await self._generate_influencer_insights(influencer_id, metrics)

        # Recommandations
        recommendations = await self._generate_influencer_recommendations(influencer_id, metrics)

        # Top content
        top_content = await self._get_top_content(influencer_id, current_period)

        return {
            'period': period,
            'metrics': metrics,
            'insights': insights,
            'recommendations': recommendations,
            'top_content': top_content,
            'generated_at': datetime.now().isoformat()
        }

    async def _generate_influencer_insights(
        self,
        influencer_id: str,
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Insights pour influenceurs"""
        insights = []

        # Growth insight
        growth = metrics['audience']['followers_growth_rate']
        if growth > 10:
            insights.append({
                'type': 'positive',
                'title': 'Croissance exceptionnelle',
                'message': f"+{growth:.1f}% de followers ce mois!",
                'action': 'Maintenez votre rythme de publication'
            })

        # Engagement insight
        engagement = metrics['content']['avg_engagement_rate']
        if engagement > 8:
            insights.append({
                'type': 'positive',
                'title': 'Engagement excellent',
                'message': f"{engagement:.1f}% d'engagement moyen",
                'action': 'Augmentez la fréquence pour maximiser l\'impact'
            })
        elif engagement < 2:
            insights.append({
                'type': 'warning',
                'title': 'Engagement faible',
                'message': f"Seulement {engagement:.1f}% d'engagement",
                'action': 'Testez de nouveaux formats (Reels, Stories)'
            })

        # Sales performance
        if metrics['sales']['conversion_rate'] > 5:
            insights.append({
                'type': 'positive',
                'title': 'Excellent convertisseur',
                'message': f"{metrics['sales']['conversion_rate']:.1f}% de conversion",
                'action': 'Demandez des prix plus élevés aux marchands'
            })

        return insights

    async def _generate_influencer_recommendations(
        self,
        influencer_id: str,
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Recommandations pour influenceurs"""
        recommendations = []

        # Reco: Post frequency
        if metrics['content']['total_posts'] < 15:
            recommendations.append({
                'priority': 'high',
                'title': 'Augmentez votre fréquence',
                'description': f"Vous n'avez publié que {metrics['content']['total_posts']} posts ce mois",
                'actions': [
                    'Publiez au moins 1 fois par jour',
                    'Utilisez l\'IA pour générer du contenu',
                    'Planifiez vos posts à l\'avance'
                ],
                'estimated_impact': '+40% engagement'
            })

        # Reco: Diversify content
        recommendations.append({
            'priority': 'medium',
            'title': 'Diversifiez vos formats',
            'description': 'Testez de nouveaux types de contenu',
            'actions': [
                'Créez des Reels (meilleure reach)',
                'Faites des Stories quotidiennes',
                'Testez les Lives pour l\'interaction'
            ],
            'estimated_impact': '+25% reach'
        })

        # Reco: Collaborate more
        if metrics['campaigns']['total_active'] < 3:
            recommendations.append({
                'priority': 'high',
                'title': 'Multipliez les collaborations',
                'description': 'Seulement {metrics["campaigns"]["total_active"]} campagnes actives',
                'actions': [
                    'Acceptez plus d\'invitations marchands',
                    'Proposez des packages attractifs',
                    'Négociez des partenariats long terme'
                ],
                'estimated_impact': '+200% revenus'
            })

        return recommendations

    async def _get_top_content(
        self,
        influencer_id: str,
        period: Dict[str, datetime]
    ) -> List[Dict[str, Any]]:
        """Top posts par performance"""
        return []

    # ========================================
    # COMMERCIAUX ANALYTICS
    # ========================================

    async def get_sales_rep_analytics(
        self,
        sales_rep_id: str,
        period: str = 'month'
    ) -> Dict[str, Any]:
        """
        Analytics complets pour commerciaux

        Returns:
            Métriques + insights + recommandations
        """
        current_period = self._get_period_dates(period)

        # Métriques
        metrics = {
            'performance': {
                'total_deals': 0,
                'deals_won': 0,
                'deals_lost': 0,
                'win_rate': 0,
                'total_revenue': 0,
                'average_deal_size': 0
            },
            'activity': {
                'total_calls': 0,
                'total_emails': 0,
                'total_meetings': 0,
                'total_demos': 0
            },
            'pipeline': {
                'total_leads': 0,
                'qualified_leads': 0,
                'qualification_rate': 0,
                'pipeline_value': 0
            },
            'efficiency': {
                'calls_per_day': 0,
                'conversion_rate': 0,
                'average_sales_cycle': 0,  # jours
                'response_time': 0  # heures
            }
        }

        # Insights
        insights = await self._generate_sales_rep_insights(sales_rep_id, metrics)

        # Recommandations
        recommendations = await self._generate_sales_rep_recommendations(sales_rep_id, metrics)

        return {
            'period': period,
            'metrics': metrics,
            'insights': insights,
            'recommendations': recommendations,
            'generated_at': datetime.now().isoformat()
        }

    async def _generate_sales_rep_insights(
        self,
        sales_rep_id: str,
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Insights pour commerciaux"""
        insights = []

        # Win rate insight
        win_rate = metrics['performance']['win_rate']
        if win_rate > 50:
            insights.append({
                'type': 'positive',
                'title': 'Excellent closer',
                'message': f"{win_rate:.0f}% de taux de closing",
                'action': 'Partagez vos techniques avec l\'équipe'
            })
        elif win_rate < 20:
            insights.append({
                'type': 'warning',
                'title': 'Taux de closing faible',
                'message': f"Seulement {win_rate:.0f}% de deals fermés",
                'action': 'Suivez une formation sur les techniques de closing'
            })

        # Activity insight
        calls_per_day = metrics['efficiency']['calls_per_day']
        if calls_per_day < 10:
            insights.append({
                'type': 'info',
                'title': 'Augmentez votre activité',
                'message': f"Seulement {calls_per_day:.0f} appels/jour",
                'action': 'Visez 20+ appels quotidiens'
            })

        return insights

    async def _generate_sales_rep_recommendations(
        self,
        sales_rep_id: str,
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Recommandations pour commerciaux"""
        recommendations = []

        # Reco: Increase activity
        if metrics['activity']['total_calls'] < 100:
            recommendations.append({
                'priority': 'high',
                'title': 'Intensifiez votre prospection',
                'description': 'Pas assez d\'appels ce mois',
                'actions': [
                    'Passez 20 appels minimum par jour',
                    'Utilisez le dialer automatique',
                    'Priorisez les leads HOT (score >70)'
                ],
                'estimated_impact': '+50% deals'
            })

        # Reco: Improve conversion
        if metrics['efficiency']['conversion_rate'] < 15:
            recommendations.append({
                'priority': 'high',
                'title': 'Améliorez votre conversion',
                'description': 'Taux de conversion en dessous de la moyenne',
                'actions': [
                    'Qualifiez mieux vos leads avant l\'appel',
                    'Personnalisez votre pitch',
                    'Pratiquez les techniques d\'objection'
                ],
                'estimated_impact': '+30% deals'
            })

        # Reco: Follow-up
        recommendations.append({
            'priority': 'medium',
            'title': 'Optimisez vos follow-ups',
            'description': 'Ne laissez pas vos prospects refroidir',
            'actions': [
                'Suivez chaque lead dans les 24h',
                'Programmez 3-5 touches minimum',
                'Utilisez l\'automation pour les rappels'
            ],
            'estimated_impact': '+25% closing'
        })

        return recommendations

    # ========================================
    # HELPER FUNCTIONS
    # ========================================

    def _get_period_dates(self, period: str) -> Dict[str, datetime]:
        """Calculer dates de la période"""
        now = datetime.now()

        if period == 'week':
            start = now - timedelta(days=7)
        elif period == 'month':
            start = now.replace(day=1)
        elif period == 'quarter':
            quarter_month = ((now.month - 1) // 3) * 3 + 1
            start = now.replace(month=quarter_month, day=1)
        elif period == 'year':
            start = now.replace(month=1, day=1)
        else:
            start = now - timedelta(days=30)

        return {'start': start, 'end': now}

    def _get_previous_period_dates(self, period: str) -> Dict[str, datetime]:
        """Calculer dates de la période précédente"""
        current = self._get_period_dates(period)

        if period == 'week':
            delta = timedelta(days=7)
        elif period == 'month':
            delta = timedelta(days=30)
        elif period == 'quarter':
            delta = timedelta(days=90)
        elif period == 'year':
            delta = timedelta(days=365)
        else:
            delta = timedelta(days=30)

        return {
            'start': current['start'] - delta,
            'end': current['end'] - delta
        }


# Global instance
analytics_service = AdvancedAnalyticsService()
