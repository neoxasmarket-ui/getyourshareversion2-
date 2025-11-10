"""
Real-time Analytics Dashboard avec WebSocket
Métriques business en temps réel pour décisions instantanées
"""
import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import redis
from fastapi import WebSocket, WebSocketDisconnect

from utils.logger import logger


class RealtimeAnalytics:
    """Service d'analytics temps réel avec WebSocket"""

    def __init__(self):
        # Redis pour pub/sub et caching
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )

        # Connexions WebSocket actives
        self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)

        # Métriques en mémoire (cache rapide)
        self.metrics_cache = {
            'sales_per_minute': 0,
            'active_users': 0,
            'conversion_rate': 0.0,
            'revenue_today': 0.0,
            'top_products': [],
            'active_sessions': {},
            'alerts': []
        }

        # Démarrer les tâches de fond
        asyncio.create_task(self._background_metrics_updater())

    async def connect(self, websocket: WebSocket, user_id: str, dashboard_type: str = "general"):
        """Connecter un client WebSocket"""
        await websocket.accept()
        self.active_connections[dashboard_type].append(websocket)

        logger.info(f"WebSocket connected: user={user_id}, type={dashboard_type}")

        # Envoyer snapshot initial
        await self.send_snapshot(websocket, dashboard_type)

    async def disconnect(self, websocket: WebSocket, dashboard_type: str = "general"):
        """Déconnecter un client"""
        if websocket in self.active_connections[dashboard_type]:
            self.active_connections[dashboard_type].remove(websocket)
            logger.info(f"WebSocket disconnected: type={dashboard_type}")

    async def send_snapshot(self, websocket: WebSocket, dashboard_type: str):
        """Envoyer snapshot complet des métriques"""
        try:
            snapshot = await self.get_dashboard_data(dashboard_type)
            await websocket.send_json({
                'type': 'snapshot',
                'timestamp': datetime.utcnow().isoformat(),
                'data': snapshot
            })
        except Exception as e:
            logger.error(f"Error sending snapshot: {e}")

    async def broadcast_metric(self, metric_type: str, data: Any, dashboard_type: str = "general"):
        """Broadcaster une métrique à tous les clients connectés"""
        message = {
            'type': 'metric_update',
            'metric': metric_type,
            'value': data,
            'timestamp': datetime.utcnow().isoformat()
        }

        disconnected = []

        for websocket in self.active_connections[dashboard_type]:
            try:
                await websocket.send_json(message)
            except WebSocketDisconnect:
                disconnected.append(websocket)
            except Exception as e:
                logger.error(f"Error broadcasting to websocket: {e}")
                disconnected.append(websocket)

        # Nettoyer les connexions mortes
        for ws in disconnected:
            await self.disconnect(ws, dashboard_type)

    async def track_sale(self, sale_data: Dict[str, Any]):
        """Tracker une vente en temps réel"""
        # Incrémenter compteurs
        self.metrics_cache['sales_per_minute'] += 1
        self.metrics_cache['revenue_today'] += float(sale_data.get('amount', 0))

        # Publier via Redis pub/sub
        await self._publish_event('sale', sale_data)

        # Broadcaster aux dashboards
        await self.broadcast_metric('new_sale', {
            'product_id': sale_data.get('product_id'),
            'amount': sale_data.get('amount'),
            'merchant': sale_data.get('merchant_name'),
            'location': sale_data.get('location')
        })

        # Mettre à jour top products
        await self._update_top_products(sale_data.get('product_id'))

        logger.info(f"Sale tracked: {sale_data.get('product_id')} - {sale_data.get('amount')}€")

    async def track_user_activity(self, user_id: str, action: str, page: str):
        """Tracker l'activité utilisateur"""
        session_key = f"session:{user_id}"

        # Stocker dans Redis avec TTL
        self.redis_client.setex(
            session_key,
            300,  # 5 minutes
            json.dumps({
                'user_id': user_id,
                'last_action': action,
                'last_page': page,
                'timestamp': datetime.utcnow().isoformat()
            })
        )

        # Mettre à jour compteur utilisateurs actifs
        active_count = len(self.redis_client.keys("session:*"))
        self.metrics_cache['active_users'] = active_count

        # Broadcaster
        await self.broadcast_metric('active_users', active_count)

    async def track_conversion(self, session_id: str, converted: bool):
        """Tracker une conversion"""
        # Calculer taux de conversion en temps réel
        total_sessions = self.redis_client.incr('total_sessions_today')

        if converted:
            conversions = self.redis_client.incr('conversions_today')
            conversion_rate = (conversions / total_sessions) * 100

            self.metrics_cache['conversion_rate'] = round(conversion_rate, 2)

            # Broadcaster
            await self.broadcast_metric('conversion_rate', conversion_rate)

    async def create_alert(self, alert_type: str, message: str, severity: str = "info"):
        """Créer une alerte temps réel"""
        alert = {
            'type': alert_type,
            'message': message,
            'severity': severity,  # info, warning, critical
            'timestamp': datetime.utcnow().isoformat()
        }

        self.metrics_cache['alerts'].append(alert)

        # Garder seulement les 50 dernières
        self.metrics_cache['alerts'] = self.metrics_cache['alerts'][-50:]

        # Broadcaster
        await self.broadcast_metric('alert', alert)

        logger.warning(f"Alert created: {alert_type} - {message}")

    async def get_dashboard_data(self, dashboard_type: str) -> Dict[str, Any]:
        """Récupérer données complètes pour un dashboard"""
        if dashboard_type == "merchant":
            return await self._get_merchant_dashboard()
        elif dashboard_type == "admin":
            return await self._get_admin_dashboard()
        else:
            return await self._get_general_dashboard()

    async def _get_general_dashboard(self) -> Dict[str, Any]:
        """Dashboard général"""
        return {
            'sales_per_minute': self.metrics_cache['sales_per_minute'],
            'active_users': self.metrics_cache['active_users'],
            'conversion_rate': self.metrics_cache['conversion_rate'],
            'revenue_today': self.metrics_cache['revenue_today'],
            'top_products': self.metrics_cache['top_products'][:10],
            'alerts': self.metrics_cache['alerts'][-10:]
        }

    async def _get_merchant_dashboard(self) -> Dict[str, Any]:
        """Dashboard merchant"""
        # Métriques spécifiques merchant
        return {
            'sales_today': await self._get_sales_today(),
            'pending_orders': await self._get_pending_orders(),
            'revenue_trend': await self._get_revenue_trend(),
            'top_products': self.metrics_cache['top_products'][:5]
        }

    async def _get_admin_dashboard(self) -> Dict[str, Any]:
        """Dashboard admin"""
        return {
            **await self._get_general_dashboard(),
            'system_health': await self._get_system_health(),
            'user_growth': await self._get_user_growth(),
            'revenue_breakdown': await self._get_revenue_breakdown()
        }

    async def _background_metrics_updater(self):
        """Tâche de fond pour mettre à jour les métriques"""
        while True:
            try:
                # Reset compteur sales per minute
                await asyncio.sleep(60)
                self.metrics_cache['sales_per_minute'] = 0

                # Nettoyer vieilles sessions
                await self._cleanup_old_sessions()

                # Calculer métriques agrégées
                await self._calculate_aggregated_metrics()

            except Exception as e:
                logger.error(f"Background updater error: {e}")

    async def _update_top_products(self, product_id: int):
        """Mettre à jour liste des produits populaires"""
        key = f"product_views:{product_id}"
        count = self.redis_client.incr(key)
        self.redis_client.expire(key, 86400)  # 24h TTL

        # Recalculer top 10
        # (Simplification - en prod utiliser Redis sorted sets)
        pass

    async def _publish_event(self, event_type: str, data: Dict[str, Any]):
        """Publier événement via Redis pub/sub"""
        try:
            self.redis_client.publish(
                f'analytics:{event_type}',
                json.dumps(data)
            )
        except Exception as e:
            logger.error(f"Redis publish error: {e}")

    async def _cleanup_old_sessions(self):
        """Nettoyer vieilles sessions"""
        # Redis TTL s'occupe déjà de ça
        pass

    async def _calculate_aggregated_metrics(self):
        """Calculer métriques agrégées"""
        # Exemple: moyenne ventes par heure
        # À implémenter selon besoins business
        pass

    async def _get_sales_today(self) -> int:
        """Nombre de ventes aujourd'hui"""
        # Requête database
        return 0  # Placeholder

    async def _get_pending_orders(self) -> int:
        """Commandes en attente"""
        return 0  # Placeholder

    async def _get_revenue_trend(self) -> List[Dict[str, Any]]:
        """Tendance revenus (dernières heures)"""
        return []  # Placeholder

    async def _get_system_health(self) -> Dict[str, Any]:
        """Santé système"""
        return {
            'cpu_usage': 0,
            'memory_usage': 0,
            'api_latency': 0
        }

    async def _get_user_growth(self) -> Dict[str, int]:
        """Croissance utilisateurs"""
        return {
            'today': 0,
            'week': 0,
            'month': 0
        }

    async def _get_revenue_breakdown(self) -> Dict[str, float]:
        """Répartition revenus"""
        return {
            'products': 0.0,
            'services': 0.0,
            'subscriptions': 0.0
        }


# Instance globale
realtime_analytics = RealtimeAnalytics()
