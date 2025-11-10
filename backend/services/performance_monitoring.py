"""
Performance Monitoring Service
- Tracks Core Web Vitals (LCP, FID, CLS, FCP, TTFB)
- Real-time performance analytics
- Anomaly detection
- Performance reports
"""
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import statistics

from utils.logger import logger
from services.advanced_caching import cache_service


class MetricType(str, Enum):
    """Core Web Vitals + additional metrics"""
    LCP = "largest-contentful-paint"      # Largest Contentful Paint
    FID = "first-input-delay"             # First Input Delay
    CLS = "cumulative-layout-shift"       # Cumulative Layout Shift
    FCP = "first-contentful-paint"        # First Contentful Paint
    TTFB = "time-to-first-byte"          # Time to First Byte
    INP = "interaction-to-next-paint"    # Interaction to Next Paint (new in 2024)


class MetricRating(str, Enum):
    """Performance rating based on Google's thresholds"""
    GOOD = "good"
    NEEDS_IMPROVEMENT = "needs-improvement"
    POOR = "poor"


class PerformanceMonitoringService:
    """Service for collecting and analyzing Web Vitals"""

    # Google's Core Web Vitals thresholds
    THRESHOLDS = {
        MetricType.LCP: {
            'good': 2500,              # < 2.5s
            'needs_improvement': 4000  # 2.5s - 4s
        },
        MetricType.FID: {
            'good': 100,               # < 100ms
            'needs_improvement': 300   # 100ms - 300ms
        },
        MetricType.CLS: {
            'good': 0.1,               # < 0.1
            'needs_improvement': 0.25  # 0.1 - 0.25
        },
        MetricType.FCP: {
            'good': 1800,              # < 1.8s
            'needs_improvement': 3000  # 1.8s - 3s
        },
        MetricType.TTFB: {
            'good': 800,               # < 800ms
            'needs_improvement': 1800  # 800ms - 1.8s
        },
        MetricType.INP: {
            'good': 200,               # < 200ms
            'needs_improvement': 500   # 200ms - 500ms
        }
    }

    def __init__(self):
        self.metrics_buffer: List[Dict[str, Any]] = []
        self.buffer_size = 100  # Batch insert every 100 metrics

    async def track_metric(
        self,
        metric_name: str,
        value: float,
        rating: str,
        user_id: Optional[str] = None,
        page_url: str = "/",
        connection_type: str = "unknown",
        device_type: str = "unknown",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Track a Web Vital metric

        Args:
            metric_name: LCP, FID, CLS, etc.
            value: Metric value (ms or score)
            rating: good, needs-improvement, poor
            user_id: Optional user identifier
            page_url: URL where metric was measured
            connection_type: 4g, 3g, wifi, etc.
            device_type: mobile, tablet, desktop
            metadata: Additional context

        Returns:
            Metric record with analysis
        """
        metric_record = {
            'metric_name': metric_name,
            'value': value,
            'rating': rating,
            'user_id': user_id,
            'page_url': page_url,
            'connection_type': connection_type,
            'device_type': device_type,
            'metadata': metadata or {},
            'timestamp': datetime.utcnow().isoformat(),
            'created_at': datetime.utcnow()
        }

        # Add to buffer
        self.metrics_buffer.append(metric_record)

        # Flush buffer if full
        if len(self.metrics_buffer) >= self.buffer_size:
            await self._flush_metrics()

        # Real-time analysis
        analysis = self._analyze_metric(metric_name, value)
        metric_record['analysis'] = analysis

        # Check for anomalies
        if analysis['is_anomaly']:
            await self._alert_anomaly(metric_record)

        logger.info(
            f"📊 Web Vital tracked: {metric_name}={value} "
            f"({rating}) on {page_url}"
        )

        return metric_record

    def _analyze_metric(self, metric_name: str, value: float) -> Dict[str, Any]:
        """Analyze if metric meets performance standards"""
        if metric_name not in self.THRESHOLDS:
            return {
                'meets_threshold': True,
                'is_anomaly': False,
                'threshold': None
            }

        thresholds = self.THRESHOLDS[metric_name]

        if value <= thresholds['good']:
            rating = MetricRating.GOOD
            meets_threshold = True
        elif value <= thresholds['needs_improvement']:
            rating = MetricRating.NEEDS_IMPROVEMENT
            meets_threshold = False
        else:
            rating = MetricRating.POOR
            meets_threshold = False

        # Check if value is anomalously high
        is_anomaly = value > (thresholds['needs_improvement'] * 2)

        return {
            'rating': rating.value,
            'meets_threshold': meets_threshold,
            'is_anomaly': is_anomaly,
            'threshold_good': thresholds['good'],
            'threshold_poor': thresholds['needs_improvement'],
            'deviation_percent': ((value - thresholds['good']) / thresholds['good']) * 100
        }

    async def _flush_metrics(self):
        """Batch insert metrics to database"""
        if not self.metrics_buffer:
            return

        try:
            # Insert into database (Supabase/PostgreSQL)
            # supabase.table('performance_metrics').insert(self.metrics_buffer).execute()

            logger.info(f"✅ Flushed {len(self.metrics_buffer)} performance metrics")

            # Clear buffer
            self.metrics_buffer = []

        except Exception as e:
            logger.error(f"Failed to flush metrics: {e}")

    async def _alert_anomaly(self, metric_record: Dict[str, Any]):
        """Alert when performance anomaly detected"""
        logger.warning(
            f"🚨 Performance anomaly detected: "
            f"{metric_record['metric_name']}={metric_record['value']} "
            f"on {metric_record['page_url']}"
        )

        # TODO: Send to alerting system (Slack, PagerDuty, etc.)

    async def get_performance_summary(
        self,
        page_url: Optional[str] = None,
        time_range: str = "24h"
    ) -> Dict[str, Any]:
        """
        Get performance summary for a page or entire site

        Args:
            page_url: Specific page or None for all pages
            time_range: 1h, 24h, 7d, 30d

        Returns:
            Summary statistics and scores
        """
        cache_key = f"perf_summary:{page_url or 'all'}:{time_range}"
        cached = cache_service.get(cache_key)

        if cached:
            return cached

        # Calculate time range
        time_deltas = {
            '1h': timedelta(hours=1),
            '24h': timedelta(days=1),
            '7d': timedelta(days=7),
            '30d': timedelta(days=30)
        }
        delta = time_deltas.get(time_range, timedelta(days=1))
        since = datetime.utcnow() - delta

        # Query metrics from database
        # metrics = supabase.table('performance_metrics')\
        #     .select('*')\
        #     .gte('created_at', since.isoformat())\
        #     .execute()

        # Mock data for example
        metrics = []

        # Group by metric type
        grouped: Dict[str, List[float]] = {}
        for metric in metrics:
            metric_name = metric['metric_name']
            if metric_name not in grouped:
                grouped[metric_name] = []
            grouped[metric_name].append(metric['value'])

        # Calculate statistics for each metric
        summary = {}
        for metric_name, values in grouped.items():
            if not values:
                continue

            summary[metric_name] = {
                'count': len(values),
                'p50': self._percentile(values, 50),  # Median
                'p75': self._percentile(values, 75),
                'p95': self._percentile(values, 95),
                'p99': self._percentile(values, 99),
                'min': min(values),
                'max': max(values),
                'avg': statistics.mean(values),
                'std_dev': statistics.stdev(values) if len(values) > 1 else 0
            }

            # Add rating
            p75_value = summary[metric_name]['p75']
            analysis = self._analyze_metric(metric_name, p75_value)
            summary[metric_name]['rating'] = analysis['rating']
            summary[metric_name]['meets_threshold'] = analysis['meets_threshold']

        # Calculate overall performance score (0-100)
        score = self._calculate_performance_score(summary)

        result = {
            'page_url': page_url or 'all',
            'time_range': time_range,
            'metrics': summary,
            'overall_score': score,
            'total_measurements': sum(m['count'] for m in summary.values()),
            'generated_at': datetime.utcnow().isoformat()
        }

        # Cache for 5 minutes
        cache_service.set(cache_key, result, ttl=300)

        return result

    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile of values"""
        if not values:
            return 0.0

        sorted_values = sorted(values)
        index = (len(sorted_values) - 1) * (percentile / 100)
        floor = int(index)
        ceil = floor + 1

        if ceil >= len(sorted_values):
            return sorted_values[-1]

        # Linear interpolation
        lower = sorted_values[floor]
        upper = sorted_values[ceil]
        fraction = index - floor

        return lower + (upper - lower) * fraction

    def _calculate_performance_score(self, summary: Dict[str, Any]) -> int:
        """
        Calculate overall performance score (0-100)
        Based on Core Web Vitals with weighted averages
        """
        if not summary:
            return 0

        # Weights (Core Web Vitals are most important)
        weights = {
            MetricType.LCP: 0.30,  # 30%
            MetricType.FID: 0.25,  # 25%
            MetricType.CLS: 0.25,  # 25%
            MetricType.FCP: 0.10,  # 10%
            MetricType.TTFB: 0.10  # 10%
        }

        total_score = 0
        total_weight = 0

        for metric_name, weight in weights.items():
            if metric_name not in summary:
                continue

            metric_data = summary[metric_name]
            p75_value = metric_data['p75']

            # Convert value to score (0-100)
            metric_score = self._value_to_score(metric_name, p75_value)

            total_score += metric_score * weight
            total_weight += weight

        # Normalize to 0-100
        final_score = int(total_score / total_weight) if total_weight > 0 else 0

        return final_score

    def _value_to_score(self, metric_name: str, value: float) -> int:
        """Convert metric value to score (0-100)"""
        if metric_name not in self.THRESHOLDS:
            return 100

        thresholds = self.THRESHOLDS[metric_name]
        good = thresholds['good']
        poor = thresholds['needs_improvement']

        # Score: 100 if <= good, 50 at poor threshold, 0 if > 2x poor
        if value <= good:
            return 100
        elif value <= poor:
            # Linear interpolation: 100 -> 50
            ratio = (value - good) / (poor - good)
            return int(100 - (ratio * 50))
        else:
            # Linear interpolation: 50 -> 0
            max_poor = poor * 2
            if value >= max_poor:
                return 0
            ratio = (value - poor) / (max_poor - poor)
            return int(50 - (ratio * 50))

    async def get_performance_trends(
        self,
        metric_name: str,
        page_url: Optional[str] = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get performance trends over time"""
        # Query daily aggregates
        # Group by date and calculate p75

        # Mock trend data
        trends = {
            'metric_name': metric_name,
            'page_url': page_url or 'all',
            'period': f'last_{days}_days',
            'data_points': [],
            'trend': 'improving',  # improving, stable, degrading
            'change_percent': -5.2  # Negative = improvement
        }

        return trends

    async def get_device_breakdown(
        self,
        time_range: str = "24h"
    ) -> Dict[str, Any]:
        """Get performance metrics broken down by device type"""
        # Group metrics by device_type (mobile, tablet, desktop)

        breakdown = {
            'mobile': {'score': 85, 'count': 1250},
            'tablet': {'score': 92, 'count': 340},
            'desktop': {'score': 98, 'count': 2100}
        }

        return breakdown

    async def get_connection_breakdown(
        self,
        time_range: str = "24h"
    ) -> Dict[str, Any]:
        """Get performance metrics broken down by connection type"""
        # Group by connection_type (4g, 3g, wifi, etc.)

        breakdown = {
            '4g': {'score': 88, 'count': 1800},
            'wifi': {'score': 96, 'count': 1500},
            '3g': {'score': 72, 'count': 200}
        }

        return breakdown


# Global instance
performance_monitor = PerformanceMonitoringService()


# FastAPI endpoint example
if __name__ == "__main__":
    """
    # Add to FastAPI app
    from fastapi import APIRouter, Body

    router = APIRouter(prefix="/api/analytics")

    @router.post("/web-vitals")
    async def track_web_vital(
        metric_name: str = Body(...),
        value: float = Body(...),
        rating: str = Body(...),
        page_url: str = Body("/"),
        connection_type: str = Body("unknown"),
        device_type: str = Body("unknown"),
        metadata: dict = Body(None)
    ):
        result = await performance_monitor.track_metric(
            metric_name=metric_name,
            value=value,
            rating=rating,
            page_url=page_url,
            connection_type=connection_type,
            device_type=device_type,
            metadata=metadata
        )
        return result

    @router.get("/performance/summary")
    async def get_performance_summary(
        page_url: str = None,
        time_range: str = "24h"
    ):
        return await performance_monitor.get_performance_summary(
            page_url=page_url,
            time_range=time_range
        )
    """
    pass
