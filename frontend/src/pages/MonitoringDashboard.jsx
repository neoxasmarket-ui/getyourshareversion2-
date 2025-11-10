/**
 * Monitoring & Observability Dashboard
 * Real-time system and application monitoring
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Icons (replace with your icon library)
const CheckIcon = () => <span className="text-green-500">✓</span>;
const AlertIcon = () => <span className="text-red-500">⚠</span>;
const InfoIcon = () => <span className="text-blue-500">ℹ</span>;

const MonitoringDashboard = () => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Fetch monitoring data
  const fetchData = async () => {
    try {
      const response = await axios.get('/api/monitoring/dashboard');
      setData(response.data);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch monitoring data:', err);
      setError('Failed to load monitoring data');
    } finally {
      setIsLoading(false);
    }
  };

  // Auto-refresh every 5 seconds
  useEffect(() => {
    fetchData();

    if (autoRefresh) {
      const interval = setInterval(fetchData, 5000);
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  if (isLoading && !data) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-indigo-500 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600">Loading monitoring data...</p>
        </div>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center text-red-600">
          <AlertIcon className="text-6xl mb-4" />
          <p>{error}</p>
        </div>
      </div>
    );
  }

  const { system, application, errors, health, recent_errors } = data || {};

  return (
    <div className="monitoring-dashboard min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Monitoring Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Real-time system and application monitoring
          </p>
        </div>

        <div className="flex items-center gap-4">
          {/* Auto-refresh toggle */}
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm text-gray-600">Auto-refresh (5s)</span>
          </label>

          {/* Manual refresh */}
          <button
            onClick={fetchData}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Health Status */}
      {health && (
        <div className="mb-6">
          <HealthStatusCard health={health} />
        </div>
      )}

      {/* System Metrics */}
      {system && (
        <div className="mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">System Metrics</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              title="CPU Usage"
              value={`${system.cpu?.percent?.toFixed(1)}%`}
              status={getStatus(system.cpu?.percent, 80, 90)}
              details={`${system.cpu?.count} cores`}
            />

            <MetricCard
              title="Memory Usage"
              value={`${system.memory?.percent?.toFixed(1)}%`}
              status={getStatus(system.memory?.percent, 80, 90)}
              details={`${system.memory?.used_gb}/${system.memory?.total_gb} GB`}
            />

            <MetricCard
              title="Disk Usage"
              value={`${system.disk?.percent?.toFixed(1)}%`}
              status={getStatus(system.disk?.percent, 80, 90)}
              details={`${system.disk?.used_gb}/${system.disk?.total_gb} GB`}
            />

            <MetricCard
              title="Uptime"
              value={system.uptime?.formatted}
              status="good"
              details={system.system?.platform}
            />
          </div>
        </div>
      )}

      {/* Application Metrics */}
      {application && (
        <div className="mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Application Metrics</h2>

          {/* Request Metrics */}
          {application.timings && (
            <div className="bg-white rounded-lg shadow-sm p-6 mb-4">
              <h3 className="font-semibold text-lg mb-4">Request Performance</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(application.timings).map(([name, metrics]) => (
                  <div key={name} className="border rounded-lg p-4">
                    <div className="text-sm text-gray-600 mb-2">{name}</div>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span>Count:</span>
                        <span className="font-semibold">{metrics.count}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Avg:</span>
                        <span className="font-semibold">{metrics.avg}ms</span>
                      </div>
                      <div className="flex justify-between">
                        <span>P95:</span>
                        <span className="font-semibold">{metrics.p95}ms</span>
                      </div>
                      <div className="flex justify-between">
                        <span>P99:</span>
                        <span className="font-semibold">{metrics.p99}ms</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Counters */}
          {application.counters && Object.keys(application.counters).length > 0 && (
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="font-semibold text-lg mb-4">Counters</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(application.counters).map(([name, value]) => (
                  <div key={name} className="border rounded-lg p-3">
                    <div className="text-2xl font-bold text-indigo-600">{value}</div>
                    <div className="text-sm text-gray-600 mt-1">{name}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error Summary */}
      {errors && (
        <div className="mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Error Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <MetricCard
              title="Total Errors"
              value={errors.total_errors || 0}
              status={errors.total_errors > 10 ? 'warning' : 'good'}
            />

            <MetricCard
              title="Unique Errors"
              value={errors.unique_errors || 0}
              status={errors.unique_errors > 5 ? 'warning' : 'good'}
            />

            <MetricCard
              title="Critical Errors"
              value={errors.errors_by_severity?.critical || 0}
              status={errors.errors_by_severity?.critical > 0 ? 'critical' : 'good'}
            />
          </div>

          {/* Top Errors */}
          {errors.top_errors && errors.top_errors.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="font-semibold text-lg mb-4">Top Errors</h3>
              <div className="space-y-2">
                {errors.top_errors.map(([errorName, count], index) => (
                  <div key={index} className="flex items-center justify-between py-2 border-b last:border-0">
                    <span className="text-sm text-gray-700">{errorName}</span>
                    <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-semibold">
                      {count}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Recent Errors */}
      {recent_errors && recent_errors.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Errors</h2>
          <div className="bg-white rounded-lg shadow-sm overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                    Timestamp
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                    Type
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                    Message
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
                    Severity
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {recent_errors.map((error, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {new Date(error.timestamp).toLocaleString()}
                    </td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">
                      {error.type}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-700">
                      {error.message}
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-semibold ${
                          error.severity === 'critical'
                            ? 'bg-red-100 text-red-700'
                            : error.severity === 'error'
                            ? 'bg-orange-100 text-orange-700'
                            : 'bg-yellow-100 text-yellow-700'
                        }`}
                      >
                        {error.severity}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

// Helper Components

const HealthStatusCard = ({ health }) => {
  const isHealthy = health.status === 'healthy';
  const isDegraded = health.status === 'degraded';

  return (
    <div
      className={`rounded-lg shadow-sm p-6 ${
        isHealthy
          ? 'bg-green-50 border-2 border-green-200'
          : isDegraded
          ? 'bg-yellow-50 border-2 border-yellow-200'
          : 'bg-red-50 border-2 border-red-200'
      }`}
    >
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold">
            {isHealthy ? (
              <span className="text-green-700">System Healthy ✓</span>
            ) : isDegraded ? (
              <span className="text-yellow-700">System Degraded ⚠</span>
            ) : (
              <span className="text-red-700">System Unhealthy ✗</span>
            )}
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Last checked: {new Date(health.timestamp).toLocaleTimeString()}
          </p>
        </div>
      </div>

      {/* Individual Checks */}
      <div className="mt-4 grid grid-cols-3 gap-4">
        {Object.entries(health.checks).map(([name, check]) => (
          <div key={name} className="flex items-center gap-2">
            {check.status === 'healthy' ? (
              <CheckIcon />
            ) : (
              <AlertIcon />
            )}
            <span className="text-sm capitalize">{name}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

const MetricCard = ({ title, value, status = 'good', details }) => {
  const statusColors = {
    good: 'border-green-200 bg-green-50',
    warning: 'border-yellow-200 bg-yellow-50',
    critical: 'border-red-200 bg-red-50'
  };

  const textColors = {
    good: 'text-green-700',
    warning: 'text-yellow-700',
    critical: 'text-red-700'
  };

  return (
    <div className={`rounded-lg shadow-sm p-6 border-2 ${statusColors[status]}`}>
      <div className="text-sm text-gray-600 mb-2">{title}</div>
      <div className={`text-3xl font-bold ${textColors[status]}`}>{value}</div>
      {details && <div className="text-sm text-gray-500 mt-2">{details}</div>}
    </div>
  );
};

// Helper function
const getStatus = (value, warningThreshold, criticalThreshold) => {
  if (value >= criticalThreshold) return 'critical';
  if (value >= warningThreshold) return 'warning';
  return 'good';
};

export default MonitoringDashboard;
