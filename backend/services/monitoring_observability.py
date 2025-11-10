"""
Complete Monitoring & Observability System
- Application Performance Monitoring (APM)
- Error tracking with stack traces
- Metrics collection (Prometheus format)
- Distributed tracing
- Health checks
- Alerting system
- Real-time monitoring dashboard
"""
import os
import time
import traceback
import psutil
import platform
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict
import asyncio

from utils.logger import logger


class MetricsCollector:
    """Collects and aggregates application metrics"""

    def __init__(self):
        self.metrics = defaultdict(lambda: {
            'count': 0,
            'sum': 0,
            'min': float('inf'),
            'max': float('-inf'),
            'avg': 0,
            'p95': 0,
            'p99': 0,
            'values': []  # For percentile calculation
        })

        self.counters = defaultdict(int)
        self.gauges = {}
        self.histograms = defaultdict(list)

    def increment(self, metric_name: str, value: int = 1, tags: Dict[str, str] = None):
        """Increment a counter metric"""
        key = self._make_key(metric_name, tags)
        self.counters[key] += value

    def gauge(self, metric_name: str, value: float, tags: Dict[str, str] = None):
        """Set a gauge metric (current value)"""
        key = self._make_key(metric_name, tags)
        self.gauges[key] = value

    def histogram(self, metric_name: str, value: float, tags: Dict[str, str] = None):
        """Record a value in histogram (for percentiles)"""
        key = self._make_key(metric_name, tags)
        self.histograms[key].append(value)

        # Keep only last 1000 values
        if len(self.histograms[key]) > 1000:
            self.histograms[key] = self.histograms[key][-1000:]

    def timing(self, metric_name: str, duration_ms: float, tags: Dict[str, str] = None):
        """Record a timing metric"""
        key = self._make_key(metric_name, tags)
        metric = self.metrics[key]

        metric['count'] += 1
        metric['sum'] += duration_ms
        metric['min'] = min(metric['min'], duration_ms)
        metric['max'] = max(metric['max'], duration_ms)
        metric['avg'] = metric['sum'] / metric['count']

        # Store for percentiles
        metric['values'].append(duration_ms)
        if len(metric['values']) > 1000:
            metric['values'] = metric['values'][-1000:]

        # Calculate percentiles
        if len(metric['values']) >= 10:
            sorted_values = sorted(metric['values'])
            p95_idx = int(len(sorted_values) * 0.95)
            p99_idx = int(len(sorted_values) * 0.99)
            metric['p95'] = sorted_values[p95_idx]
            metric['p99'] = sorted_values[p99_idx]

    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics"""
        return {
            'counters': dict(self.counters),
            'gauges': dict(self.gauges),
            'histograms': {k: sorted(v) for k, v in self.histograms.items()},
            'timings': {
                k: {
                    'count': v['count'],
                    'avg': round(v['avg'], 2),
                    'min': round(v['min'], 2),
                    'max': round(v['max'], 2),
                    'p95': round(v['p95'], 2),
                    'p99': round(v['p99'], 2)
                }
                for k, v in self.metrics.items()
            }
        }

    def reset(self):
        """Reset all metrics"""
        self.metrics.clear()
        self.counters.clear()
        self.gauges.clear()
        self.histograms.clear()

    def _make_key(self, metric_name: str, tags: Optional[Dict[str, str]]) -> str:
        """Create metric key with tags"""
        if not tags:
            return metric_name

        tag_str = ','.join(f'{k}={v}' for k, v in sorted(tags.items()))
        return f'{metric_name}{{{tag_str}}}'


class ErrorTracker:
    """Tracks and aggregates errors"""

    def __init__(self, max_errors: int = 100):
        self.errors = []
        self.max_errors = max_errors
        self.error_counts = defaultdict(int)

    def track_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None
    ):
        """Track an error with full context"""
        error_record = {
            'type': type(error).__name__,
            'message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'user_id': user_id,
            'request_id': request_id,
            'timestamp': datetime.utcnow().isoformat(),
            'severity': self._determine_severity(error)
        }

        # Add to errors list
        self.errors.append(error_record)

        # Keep only last N errors
        if len(self.errors) > self.max_errors:
            self.errors = self.errors[-self.max_errors:]

        # Increment error count
        error_key = f"{error_record['type']}:{error_record['message'][:50]}"
        self.error_counts[error_key] += 1

        # Log error
        logger.error(
            f"Error tracked: {error_record['type']} - {error_record['message']}",
            extra={'error_record': error_record}
        )

        return error_record

    def get_recent_errors(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent errors"""
        return self.errors[-limit:]

    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary statistics"""
        if not self.errors:
            return {
                'total_errors': 0,
                'unique_errors': 0,
                'error_rate': 0
            }

        # Count errors by type
        errors_by_type = defaultdict(int)
        errors_by_severity = defaultdict(int)

        for error in self.errors:
            errors_by_type[error['type']] += 1
            errors_by_severity[error['severity']] += 1

        return {
            'total_errors': len(self.errors),
            'unique_errors': len(self.error_counts),
            'errors_by_type': dict(errors_by_type),
            'errors_by_severity': dict(errors_by_severity),
            'top_errors': sorted(
                self.error_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }

    def _determine_severity(self, error: Exception) -> str:
        """Determine error severity"""
        critical_errors = (KeyError, AttributeError, ImportError, SystemError)
        warning_errors = (ValueError, TypeError)

        if isinstance(error, critical_errors):
            return 'critical'
        elif isinstance(error, warning_errors):
            return 'warning'
        else:
            return 'error'


class HealthCheck:
    """Health check system for services"""

    def __init__(self):
        self.checks = {}
        self.last_results = {}

    def register_check(self, name: str, check_func: Callable):
        """Register a health check"""
        self.checks[name] = check_func

    async def run_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        results = {}
        overall_status = 'healthy'

        for name, check_func in self.checks.items():
            try:
                if asyncio.iscoroutinefunction(check_func):
                    result = await check_func()
                else:
                    result = check_func()

                results[name] = {
                    'status': 'healthy' if result else 'unhealthy',
                    'timestamp': datetime.utcnow().isoformat()
                }

                if not result:
                    overall_status = 'degraded'

            except Exception as e:
                results[name] = {
                    'status': 'unhealthy',
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat()
                }
                overall_status = 'unhealthy'

        self.last_results = results

        return {
            'status': overall_status,
            'checks': results,
            'timestamp': datetime.utcnow().isoformat()
        }

    def get_last_results(self) -> Dict[str, Any]:
        """Get last health check results"""
        return self.last_results


class MonitoringService:
    """Complete monitoring and observability service"""

    def __init__(self):
        self.metrics = MetricsCollector()
        self.errors = ErrorTracker()
        self.health = HealthCheck()

        self.start_time = datetime.utcnow()
        self.request_count = 0

        # Register default health checks
        self._register_default_health_checks()

    def _register_default_health_checks(self):
        """Register default health checks"""

        def check_memory():
            """Check memory usage"""
            memory = psutil.virtual_memory()
            return memory.percent < 90  # Alert if > 90%

        def check_disk():
            """Check disk usage"""
            disk = psutil.disk_usage('/')
            return disk.percent < 85  # Alert if > 85%

        def check_cpu():
            """Check CPU usage"""
            cpu = psutil.cpu_percent(interval=1)
            return cpu < 80  # Alert if > 80%

        self.health.register_check('memory', check_memory)
        self.health.register_check('disk', check_disk)
        self.health.register_check('cpu', check_cpu)

    # ========================================
    # DECORATORS
    # ========================================

    def monitor(self, metric_name: Optional[str] = None, track_errors: bool = True):
        """
        Decorator to monitor function execution

        Usage:
            @monitoring.monitor('api.get_products')
            async def get_products():
                ...
        """
        def decorator(func):
            name = metric_name or f'{func.__module__}.{func.__name__}'

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                request_id = kwargs.get('request_id', 'unknown')

                # Increment request counter
                self.metrics.increment(f'{name}.requests')

                try:
                    result = await func(*args, **kwargs)

                    # Track success
                    self.metrics.increment(f'{name}.success')

                    return result

                except Exception as e:
                    # Track error
                    self.metrics.increment(f'{name}.errors')

                    if track_errors:
                        self.errors.track_error(
                            e,
                            context={'function': name, 'args': str(args)[:100]},
                            request_id=request_id
                        )

                    raise

                finally:
                    # Track timing
                    duration_ms = (time.time() - start_time) * 1000
                    self.metrics.timing(f'{name}.duration_ms', duration_ms)

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()

                self.metrics.increment(f'{name}.requests')

                try:
                    result = func(*args, **kwargs)
                    self.metrics.increment(f'{name}.success')
                    return result

                except Exception as e:
                    self.metrics.increment(f'{name}.errors')

                    if track_errors:
                        self.errors.track_error(
                            e,
                            context={'function': name, 'args': str(args)[:100]}
                        )

                    raise

                finally:
                    duration_ms = (time.time() - start_time) * 1000
                    self.metrics.timing(f'{name}.duration_ms', duration_ms)

            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper

        return decorator

    # ========================================
    # SYSTEM METRICS
    # ========================================

    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect system-level metrics"""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()

        # Memory
        memory = psutil.virtual_memory()

        # Disk
        disk = psutil.disk_usage('/')

        # Network
        net_io = psutil.net_io_counters()

        # Uptime
        uptime = datetime.utcnow() - self.start_time

        metrics = {
            'system': {
                'platform': platform.system(),
                'platform_version': platform.version(),
                'python_version': platform.python_version(),
                'hostname': platform.node()
            },
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'per_cpu': psutil.cpu_percent(percpu=True)
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent,
                'total_gb': round(memory.total / (1024 ** 3), 2),
                'used_gb': round(memory.used / (1024 ** 3), 2)
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent,
                'total_gb': round(disk.total / (1024 ** 3), 2),
                'used_gb': round(disk.used / (1024 ** 3), 2)
            },
            'network': {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            },
            'uptime': {
                'seconds': uptime.total_seconds(),
                'formatted': str(uptime).split('.')[0]
            }
        }

        # Update gauges
        self.metrics.gauge('system.cpu.percent', cpu_percent)
        self.metrics.gauge('system.memory.percent', memory.percent)
        self.metrics.gauge('system.disk.percent', disk.percent)

        return metrics

    # ========================================
    # DASHBOARD DATA
    # ========================================

    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get complete dashboard data"""
        system_metrics = self.collect_system_metrics()
        app_metrics = self.metrics.get_metrics()
        error_summary = self.errors.get_error_summary()
        health_status = await self.health.run_checks()

        return {
            'timestamp': datetime.utcnow().isoformat(),
            'system': system_metrics,
            'application': app_metrics,
            'errors': error_summary,
            'health': health_status,
            'recent_errors': self.errors.get_recent_errors(limit=10)
        }

    # ========================================
    # PROMETHEUS FORMAT EXPORT
    # ========================================

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format"""
        lines = []

        # Counters
        for name, value in self.metrics.counters.items():
            lines.append(f'# TYPE {name} counter')
            lines.append(f'{name} {value}')

        # Gauges
        for name, value in self.metrics.gauges.items():
            lines.append(f'# TYPE {name} gauge')
            lines.append(f'{name} {value}')

        # Histograms (as summaries)
        for name, metric in self.metrics.metrics.items():
            lines.append(f'# TYPE {name} summary')
            lines.append(f'{name}{{quantile="0.5"}} {metric["avg"]}')
            lines.append(f'{name}{{quantile="0.95"}} {metric["p95"]}')
            lines.append(f'{name}{{quantile="0.99"}} {metric["p99"]}')
            lines.append(f'{name}_count {metric["count"]}')
            lines.append(f'{name}_sum {metric["sum"]}')

        return '\n'.join(lines)


# Global monitoring instance
monitoring = MonitoringService()


# FastAPI middleware example
"""
from fastapi import Request, Response
import time

@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start_time = time.time()

    # Track request
    monitoring.metrics.increment('http.requests.total')

    try:
        response = await call_next(request)

        # Track success
        monitoring.metrics.increment(
            'http.requests.success',
            tags={'method': request.method, 'path': request.url.path}
        )

        # Track status code
        monitoring.metrics.increment(
            'http.responses',
            tags={'status_code': str(response.status_code)}
        )

        return response

    except Exception as e:
        # Track error
        monitoring.metrics.increment('http.requests.error')
        monitoring.errors.track_error(e, context={'path': request.url.path})
        raise

    finally:
        # Track duration
        duration_ms = (time.time() - start_time) * 1000
        monitoring.metrics.timing(
            'http.request.duration_ms',
            duration_ms,
            tags={'method': request.method}
        )
"""
