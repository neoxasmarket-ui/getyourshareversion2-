/**
 * Dashboard Commercial (Sales Representative)
 * Tableau de bord complet pour les commerciaux
 * - Vue d'ensemble KPIs
 * - Pipeline de ventes
 * - Leads & Deals
 * - Activités quotidiennes
 * - Gamification & Leaderboard
 * - Objectifs & Performance
 */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

// Icons (remplacer par votre bibliothèque d'icônes)
const TrophyIcon = () => <span className="text-yellow-500">🏆</span>;
const FireIcon = () => <span className="text-red-500">🔥</span>;
const TargetIcon = () => <span className="text-blue-500">🎯</span>;
const PhoneIcon = () => <span>📞</span>;
const EmailIcon = () => <span>📧</span>;
const MeetingIcon = () => <span>📅</span>;
const MoneyIcon = () => <span>💰</span>;
const TrendingUpIcon = () => <span>📈</span>;
const StarIcon = () => <span>⭐</span>;

const SalesRepDashboard = () => {
  const [stats, setStats] = useState(null);
  const [leads, setLeads] = useState([]);
  const [deals, setDeals] = useState([]);
  const [activities, setActivities] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('month'); // week, month, quarter

  // Fetch données
  useEffect(() => {
    fetchDashboardData();
  }, [selectedPeriod]);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    try {
      const [statsRes, leadsRes, dealsRes, leaderboardRes] = await Promise.all([
        axios.get('/api/sales/dashboard/me'),
        axios.get('/api/sales/leads/me?status=active&sort=score'),
        axios.get('/api/sales/deals/me?period=' + selectedPeriod),
        axios.get('/api/sales/leaderboard?period=' + selectedPeriod)
      ]);

      setStats(statsRes.data);
      setLeads(leadsRes.data.results || []);
      setDeals(dealsRes.data.results || []);
      setLeaderboard(leaderboardRes.data || []);
    } catch (error) {
      console.error('Erreur chargement dashboard:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && !stats) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-indigo-500 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement de votre dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="sales-rep-dashboard min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Tableau de Bord Commercial
            </h1>
            <p className="text-gray-600 mt-1">
              Bienvenue, {stats?.sales_rep?.first_name}! 👋
            </p>
          </div>

          {/* Period Selector */}
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="px-4 py-2 border rounded-lg bg-white"
          >
            <option value="week">Cette semaine</option>
            <option value="month">Ce mois</option>
            <option value="quarter">Ce trimestre</option>
            <option value="year">Cette année</option>
          </select>
        </div>
      </div>

      {/* KPIs Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <KPICard
          title="Deals Fermés"
          value={stats?.this_month?.deals || 0}
          subtitle="Ce mois"
          icon={<TrophyIcon />}
          color="blue"
          trend={stats?.trends?.deals_pct || 0}
        />

        <KPICard
          title="Revenu Généré"
          value={`${(stats?.this_month?.revenue || 0).toLocaleString()} MAD`}
          subtitle="Ce mois"
          icon={<MoneyIcon />}
          color="green"
          trend={stats?.trends?.revenue_pct || 0}
        />

        <KPICard
          title="Commission"
          value={`${(stats?.overview?.commission_earned || 0).toLocaleString()} MAD`}
          subtitle="Total gagné"
          icon={<MoneyIcon />}
          color="purple"
        />

        <KPICard
          title="Taux Conversion"
          value={`${(stats?.overview?.conversion_rate || 0).toFixed(1)}%`}
          subtitle="Performance globale"
          icon={<TrendingUpIcon />}
          color="orange"
        />
      </div>

      {/* Gamification & Leaderboard */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Gamification Card */}
        <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg shadow-lg p-6 text-white">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <StarIcon /> Votre Niveau
          </h3>

          <div className="text-center mb-4">
            <div className="text-5xl font-bold mb-2">
              {stats?.gamification?.level_tier?.toUpperCase() || 'BRONZE'}
            </div>
            <div className="text-sm opacity-90">
              {stats?.gamification?.points || 0} points
            </div>
          </div>

          {/* Progress Bar */}
          <div className="bg-white bg-opacity-20 rounded-full h-4 mb-2">
            <div
              className="bg-white rounded-full h-4 transition-all duration-500"
              style={{
                width: `${((stats?.gamification?.points || 0) / (stats?.gamification?.next_level_points || 5000)) * 100}%`
              }}
            ></div>
          </div>
          <div className="text-xs text-center opacity-90">
            {(stats?.gamification?.next_level_points || 5000) - (stats?.gamification?.points || 0)} points
            pour le prochain niveau
          </div>

          {/* Badges */}
          {stats?.gamification?.badges?.length > 0 && (
            <div className="mt-4 pt-4 border-t border-white border-opacity-20">
              <div className="text-sm mb-2">Badges récents:</div>
              <div className="flex flex-wrap gap-2">
                {stats.gamification.badges.slice(0, 3).map((badge, idx) => (
                  <span key={idx} className="px-2 py-1 bg-white bg-opacity-20 rounded text-xs">
                    {badge}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Leaderboard */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <TrophyIcon /> Classement
          </h3>

          {leaderboard.length > 0 ? (
            <div className="space-y-3">
              {leaderboard.slice(0, 5).map((rep, index) => (
                <div
                  key={rep.id}
                  className={`flex items-center justify-between p-3 rounded-lg ${
                    index === 0
                      ? 'bg-yellow-50 border-2 border-yellow-300'
                      : index === 1
                      ? 'bg-gray-100'
                      : index === 2
                      ? 'bg-orange-50'
                      : 'bg-gray-50'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className="text-2xl font-bold text-gray-400">
                      #{index + 1}
                    </div>
                    <div>
                      <div className="font-semibold">
                        {rep.first_name} {rep.last_name}
                      </div>
                      <div className="text-sm text-gray-600">
                        {rep.territory}
                      </div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="font-bold text-indigo-600">
                      {rep.total_deals} deals
                    </div>
                    <div className="text-sm text-gray-600">
                      {rep.total_revenue?.toLocaleString()} MAD
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              Aucune donnée disponible
            </div>
          )}
        </div>
      </div>

      {/* Objectifs & Pipeline */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Objectifs du Mois */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <TargetIcon /> Objectifs du Mois
          </h3>

          <div className="space-y-4">
            {/* Objectif Deals */}
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm text-gray-600">Deals</span>
                <span className="text-sm font-semibold">
                  {stats?.this_month?.deals || 0} / {stats?.targets?.deals_target || 20}
                </span>
              </div>
              <div className="bg-gray-200 rounded-full h-3">
                <div
                  className="bg-blue-500 rounded-full h-3 transition-all"
                  style={{
                    width: `${Math.min(((stats?.this_month?.deals || 0) / (stats?.targets?.deals_target || 20)) * 100, 100)}%`
                  }}
                ></div>
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {stats?.targets?.deals_completion_pct || 0}% atteint
              </div>
            </div>

            {/* Objectif Revenu */}
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm text-gray-600">Revenu</span>
                <span className="text-sm font-semibold">
                  {(stats?.this_month?.revenue || 0).toLocaleString()} / {(stats?.targets?.revenue_target || 100000).toLocaleString()} MAD
                </span>
              </div>
              <div className="bg-gray-200 rounded-full h-3">
                <div
                  className="bg-green-500 rounded-full h-3 transition-all"
                  style={{
                    width: `${Math.min(((stats?.this_month?.revenue || 0) / (stats?.targets?.revenue_target || 100000)) * 100, 100)}%`
                  }}
                ></div>
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {stats?.targets?.revenue_completion_pct || 0}% atteint
              </div>
            </div>

            {/* Objectif Appels */}
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm text-gray-600">Appels</span>
                <span className="text-sm font-semibold">
                  {stats?.this_month?.calls || 0} / {stats?.targets?.calls_target || 100}
                </span>
              </div>
              <div className="bg-gray-200 rounded-full h-3">
                <div
                  className="bg-purple-500 rounded-full h-3 transition-all"
                  style={{
                    width: `${Math.min(((stats?.this_month?.calls || 0) / (stats?.targets?.calls_target || 100)) * 100, 100)}%`
                  }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Pipeline de Ventes */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold mb-4">Pipeline de Ventes</h3>

          <div className="space-y-3">
            {[
              { status: 'new', label: 'Nouveaux', count: stats?.pipeline?.new || 0, color: 'bg-gray-500' },
              { status: 'contacted', label: 'Contactés', count: stats?.pipeline?.contacted || 0, color: 'bg-blue-500' },
              { status: 'qualified', label: 'Qualifiés', count: stats?.pipeline?.qualified || 0, color: 'bg-indigo-500' },
              { status: 'proposal', label: 'Proposition', count: stats?.pipeline?.proposal || 0, color: 'bg-purple-500' },
              { status: 'negotiation', label: 'Négociation', count: stats?.pipeline?.negotiation || 0, color: 'bg-orange-500' }
            ].map((stage) => (
              <div key={stage.status} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className={`w-3 h-3 rounded-full ${stage.color}`}></div>
                  <span className="text-sm">{stage.label}</span>
                </div>
                <span className="font-semibold">{stage.count}</span>
              </div>
            ))}

            <div className="pt-3 border-t">
              <div className="flex items-center justify-between font-bold">
                <span>Valeur Totale</span>
                <span className="text-indigo-600">
                  {(stats?.pipeline?.total_value || 0).toLocaleString()} MAD
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Leads HOT */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <FireIcon /> Leads HOT (Score élevé)
          </h3>
          <Link
            to="/sales/leads"
            className="text-sm text-indigo-600 hover:text-indigo-700"
          >
            Voir tous les leads →
          </Link>
        </div>

        {leads.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">
                    Score
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">
                    Contact
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">
                    Entreprise
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">
                    Valeur Estimée
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">
                    Statut
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {leads.slice(0, 5).map((lead) => (
                  <tr key={lead.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full font-bold ${
                        lead.score >= 80
                          ? 'bg-green-100 text-green-700'
                          : lead.score >= 60
                          ? 'bg-yellow-100 text-yellow-700'
                          : 'bg-gray-100 text-gray-700'
                      }`}>
                        {lead.score}
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="font-medium">{lead.contact_name}</div>
                      <div className="text-sm text-gray-600">{lead.contact_email}</div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="text-sm">{lead.company_name || '-'}</div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="font-semibold text-indigo-600">
                        {lead.estimated_value?.toLocaleString() || 0} MAD
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                        lead.lead_status === 'new'
                          ? 'bg-gray-100 text-gray-700'
                          : lead.lead_status === 'qualified'
                          ? 'bg-blue-100 text-blue-700'
                          : 'bg-green-100 text-green-700'
                      }`}>
                        {lead.lead_status}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex gap-2">
                        <button className="p-2 hover:bg-gray-100 rounded">
                          <PhoneIcon />
                        </button>
                        <button className="p-2 hover:bg-gray-100 rounded">
                          <EmailIcon />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center text-gray-500 py-8">
            Aucun lead actif
          </div>
        )}
      </div>

      {/* Activités Quotidiennes */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold mb-4">Aujourd'hui</h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-3 mb-2">
              <PhoneIcon />
              <span className="text-sm text-gray-600">Appels programmés</span>
            </div>
            <div className="text-2xl font-bold">{stats?.today?.calls_scheduled || 0}</div>
          </div>

          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-3 mb-2">
              <MeetingIcon />
              <span className="text-sm text-gray-600">Réunions</span>
            </div>
            <div className="text-2xl font-bold">{stats?.today?.meetings_scheduled || 0}</div>
          </div>

          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-3 mb-2">
              <TargetIcon />
              <span className="text-sm text-gray-600">Tâches en attente</span>
            </div>
            <div className="text-2xl font-bold">{stats?.today?.tasks_pending || 0}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Composant KPI Card
const KPICard = ({ title, value, subtitle, icon, color, trend }) => {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    orange: 'bg-orange-50 text-orange-600'
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-2">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          {icon}
        </div>
        {trend !== undefined && (
          <div className={`text-sm font-semibold ${trend >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {trend >= 0 ? '+' : ''}{trend}%
          </div>
        )}
      </div>
      <div className="text-2xl font-bold text-gray-900 mb-1">{value}</div>
      <div className="text-sm text-gray-600">{subtitle}</div>
    </div>
  );
};

export default SalesRepDashboard;
