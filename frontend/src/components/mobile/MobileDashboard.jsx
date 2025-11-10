import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Phone, Mail, MessageCircle, TrendingUp, Target, Award,
  DollarSign, BarChart2, Users, Zap, ChevronRight, Bell
} from 'lucide-react';
import QuickActions from './QuickActions';
import BottomNavigation from './BottomNavigation';

/**
 * Mobile-optimized dashboard for all user types
 * Responsive, touch-friendly, works offline
 */
const MobileDashboard = ({ userType = 'merchant', userId }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    fetchDashboardData();
    requestNotificationPermission();
  }, [userType, userId]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      let endpoint = '';

      if (userType === 'merchant') {
        endpoint = `/api/merchants/${userId}/dashboard`;
      } else if (userType === 'influencer') {
        endpoint = `/api/influencers/${userId}/dashboard`;
      } else if (userType === 'sales_rep') {
        endpoint = `/api/sales/dashboard/${userId}`;
      }

      const response = await axios.get(endpoint);
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      // Try to load from cache if offline
      const cachedData = localStorage.getItem(`dashboard_${userType}_${userId}`);
      if (cachedData) {
        setStats(JSON.parse(cachedData));
      }
      setLoading(false);
    }
  };

  const requestNotificationPermission = async () => {
    if ('Notification' in window && Notification.permission === 'default') {
      await Notification.requestPermission();
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-blue-500 to-purple-600">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-white mx-auto mb-4"></div>
          <p className="text-white text-lg">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="mobile-dashboard min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <MobileHeader userType={userType} notifications={notifications} />

      {/* Quick Stats Cards */}
      <div className="p-4 space-y-4">
        {userType === 'merchant' && <MerchantStats stats={stats} />}
        {userType === 'influencer' && <InfluencerStats stats={stats} />}
        {userType === 'sales_rep' && <SalesRepStats stats={stats} />}
      </div>

      {/* Quick Actions */}
      <div className="px-4 mb-6">
        <QuickActions userType={userType} userId={userId} />
      </div>

      {/* Recent Activity */}
      <RecentActivity userType={userType} stats={stats} />

      {/* Bottom Navigation */}
      <BottomNavigation userType={userType} />
    </div>
  );
};

// ==================== HEADER ====================
const MobileHeader = ({ userType, notifications }) => {
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Bonjour';
    if (hour < 18) return 'Bon après-midi';
    return 'Bonsoir';
  };

  const getTypeLabel = () => {
    if (userType === 'merchant') return 'Marchand';
    if (userType === 'influencer') return 'Influenceur';
    return 'Commercial';
  };

  return (
    <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-b-3xl shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold">{getGreeting()} 👋</h1>
          <p className="text-blue-100 text-sm mt-1">{getTypeLabel()}</p>
        </div>
        <div className="relative">
          <button className="relative p-2 bg-white bg-opacity-20 rounded-full">
            <Bell className="h-6 w-6" />
            {notifications.length > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {notifications.length}
              </span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

// ==================== STATS ====================
const MerchantStats = ({ stats }) => {
  const cards = [
    {
      icon: DollarSign,
      label: 'Revenu ce mois',
      value: `${stats?.revenue?.toLocaleString() || 0} MAD`,
      trend: stats?.revenue_trend || 0,
      color: 'from-green-400 to-green-600'
    },
    {
      icon: BarChart2,
      label: 'Commandes',
      value: stats?.orders || 0,
      trend: stats?.orders_trend || 0,
      color: 'from-blue-400 to-blue-600'
    },
    {
      icon: Users,
      label: 'Clients',
      value: stats?.customers || 0,
      trend: stats?.customers_trend || 0,
      color: 'from-purple-400 to-purple-600'
    },
    {
      icon: Award,
      label: 'Note',
      value: `${stats?.rating?.toFixed(1) || 0}/5`,
      trend: stats?.rating_trend || 0,
      color: 'from-yellow-400 to-yellow-600'
    }
  ];

  return <StatCards cards={cards} />;
};

const InfluencerStats = ({ stats }) => {
  const cards = [
    {
      icon: DollarSign,
      label: 'Commission',
      value: `${stats?.commission?.toLocaleString() || 0} MAD`,
      trend: stats?.commission_trend || 0,
      color: 'from-green-400 to-green-600'
    },
    {
      icon: TrendingUp,
      label: 'Ventes',
      value: stats?.sales || 0,
      trend: stats?.sales_trend || 0,
      color: 'from-blue-400 to-blue-600'
    },
    {
      icon: Users,
      label: 'Followers',
      value: (stats?.followers || 0).toLocaleString(),
      trend: stats?.followers_trend || 0,
      color: 'from-purple-400 to-purple-600'
    },
    {
      icon: Zap,
      label: 'Engagement',
      value: `${stats?.engagement?.toFixed(1) || 0}%`,
      trend: stats?.engagement_trend || 0,
      color: 'from-pink-400 to-pink-600'
    }
  ];

  return <StatCards cards={cards} />;
};

const SalesRepStats = ({ stats }) => {
  const cards = [
    {
      icon: Target,
      label: 'Deals fermés',
      value: stats?.deals || 0,
      trend: stats?.deals_trend || 0,
      color: 'from-blue-400 to-blue-600'
    },
    {
      icon: DollarSign,
      label: 'Revenu généré',
      value: `${stats?.revenue?.toLocaleString() || 0} MAD`,
      trend: stats?.revenue_trend || 0,
      color: 'from-green-400 to-green-600'
    },
    {
      icon: Phone,
      label: 'Appels',
      value: stats?.calls || 0,
      trend: stats?.calls_trend || 0,
      color: 'from-orange-400 to-orange-600'
    },
    {
      icon: Award,
      label: 'Taux closing',
      value: `${stats?.win_rate?.toFixed(0) || 0}%`,
      trend: stats?.win_rate_trend || 0,
      color: 'from-purple-400 to-purple-600'
    }
  ];

  return <StatCards cards={cards} />;
};

const StatCards = ({ cards }) => {
  return (
    <div className="grid grid-cols-2 gap-4">
      {cards.map((card, index) => (
        <StatCard key={index} {...card} />
      ))}
    </div>
  );
};

const StatCard = ({ icon: Icon, label, value, trend, color }) => {
  const trendColor = trend > 0 ? 'text-green-600' : trend < 0 ? 'text-red-600' : 'text-gray-600';
  const trendSymbol = trend > 0 ? '↑' : trend < 0 ? '↓' : '→';

  return (
    <div className="bg-white rounded-2xl shadow-md p-4 transform hover:scale-105 transition">
      <div className={`bg-gradient-to-br ${color} w-12 h-12 rounded-xl flex items-center justify-center mb-3`}>
        <Icon className="h-6 w-6 text-white" />
      </div>
      <p className="text-gray-600 text-xs mb-1">{label}</p>
      <p className="text-xl font-bold text-gray-900">{value}</p>
      <p className={`text-xs font-medium mt-1 ${trendColor}`}>
        {trendSymbol} {Math.abs(trend).toFixed(1)}%
      </p>
    </div>
  );
};

// ==================== RECENT ACTIVITY ====================
const RecentActivity = ({ userType, stats }) => {
  if (!stats?.recent_activity || stats.recent_activity.length === 0) return null;

  return (
    <div className="px-4 mb-6">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg font-bold text-gray-900">Activité Récente</h2>
        <button className="text-blue-600 text-sm font-medium">Tout voir</button>
      </div>

      <div className="bg-white rounded-2xl shadow-md overflow-hidden">
        {stats.recent_activity.map((activity, index) => (
          <div
            key={index}
            className="flex items-center justify-between p-4 border-b last:border-b-0 hover:bg-gray-50 active:bg-gray-100 transition"
          >
            <div className="flex items-center space-x-3">
              <div className={`w-10 h-10 rounded-full ${getActivityColor(activity.type)} flex items-center justify-center`}>
                {getActivityIcon(activity.type)}
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">{activity.title}</p>
                <p className="text-xs text-gray-500">{activity.time}</p>
              </div>
            </div>
            <ChevronRight className="h-5 w-5 text-gray-400" />
          </div>
        ))}
      </div>
    </div>
  );
};

const getActivityColor = (type) => {
  const colors = {
    sale: 'bg-green-100',
    lead: 'bg-blue-100',
    call: 'bg-orange-100',
    meeting: 'bg-purple-100',
    content: 'bg-pink-100'
  };
  return colors[type] || 'bg-gray-100';
};

const getActivityIcon = (type) => {
  const icons = {
    sale: <DollarSign className="h-5 w-5 text-green-600" />,
    lead: <Target className="h-5 w-5 text-blue-600" />,
    call: <Phone className="h-5 w-5 text-orange-600" />,
    meeting: <Users className="h-5 w-5 text-purple-600" />,
    content: <Zap className="h-5 w-5 text-pink-600" />
  };
  return icons[type] || null;
};

export default MobileDashboard;
