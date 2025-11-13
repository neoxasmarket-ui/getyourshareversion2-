import React, { useEffect, useState } from 'react';
import api from '../../utils/api';
import Card from '../../components/common/Card';
import Table from '../../components/common/Table';
import Badge from '../../components/common/Badge';
import Button from '../../components/common/Button';
import { formatCurrency, formatDate } from '../../utils/helpers';
import { 
  Check, X, DollarSign, Clock, CheckCircle, XCircle, 
  CreditCard, TrendingUp, Users, Calendar, Search,
  Filter, Mail, Eye, ExternalLink
} from 'lucide-react';
import {
  AreaChart, Area, PieChart, Pie, Cell, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const AffiliatePayouts = () => {
  const [payouts, setPayouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterMethod, setFilterMethod] = useState('all');
  const [selectedPayout, setSelectedPayout] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  const [animatedValues, setAnimatedValues] = useState({
    total: 0,
    pending: 0,
    approved: 0,
    paid: 0
  });
  const [hoveredCard, setHoveredCard] = useState(null);

  useEffect(() => {
    fetchPayouts();
  }, []);

  useEffect(() => {
    if (payouts.length > 0) {
      const stats = calculateStats();
      animateValue(0, stats.total, 1500, 'total');
      animateValue(0, stats.pending, 1500, 'pending');
      animateValue(0, stats.approved, 1500, 'approved');
      animateValue(0, stats.paid, 1500, 'paid');
    }
  }, [payouts]);

  const animateValue = (start, end, duration, key) => {
    const startTime = Date.now();
    const animate = () => {
      const now = Date.now();
      const progress = Math.min((now - startTime) / duration, 1);
      const easeOutCubic = 1 - Math.pow(1 - progress, 3);
      const value = start + (end - start) * easeOutCubic;
      setAnimatedValues(prev => ({ ...prev, [key]: Math.floor(value) }));
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    requestAnimationFrame(animate);
  };

  const calculateStats = () => {
    const total = payouts.length;
    const pending = payouts.filter(p => p.status === 'pending').length;
    const approved = payouts.filter(p => p.status === 'approved').length;
    const paid = payouts.filter(p => p.status === 'paid').length;
    const totalAmount = payouts.reduce((sum, p) => sum + (parseFloat(p.amount) || 0), 0);
    const pendingAmount = payouts.filter(p => p.status === 'pending').reduce((sum, p) => sum + (parseFloat(p.amount) || 0), 0);
    const paidAmount = payouts.filter(p => p.status === 'paid').reduce((sum, p) => sum + (parseFloat(p.amount) || 0), 0);
    
    return { total, pending, approved, paid, totalAmount, pendingAmount, paidAmount };
  };

  const fetchPayouts = async () => {
    try {
      const response = await api.get('/api/payouts');
      setPayouts(response.data.data);
    } catch (error) {
      console.error('Error fetching payouts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id) => {
    try {
      await api.put(`/api/payouts/${id}/status`, { status: 'approved' });
      fetchPayouts();
      if (showDetails && selectedPayout?.id === id) {
        setShowDetails(false);
        setSelectedPayout(null);
      }
    } catch (error) {
      console.error('Error approving payout:', error);
    }
  };

  const handleReject = async (id) => {
    try {
      await api.put(`/api/payouts/${id}/status`, { status: 'rejected' });
      fetchPayouts();
      if (showDetails && selectedPayout?.id === id) {
        setShowDetails(false);
        setSelectedPayout(null);
      }
    } catch (error) {
      console.error('Error rejecting payout:', error);
    }
  };

  const handleViewDetails = (payout) => {
    setSelectedPayout(payout);
    setShowDetails(true);
  };

  // Filter payouts based on search and filters
  const filteredPayouts = payouts.filter(payout => {
    const affiliateName = payout.influencers?.full_name || payout.influencers?.username || payout.affiliate_name || '';
    const matchesSearch = affiliateName.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || payout.status === filterStatus;
    const paymentMethod = payout.payment_method || payout.method || 'N/A';
    const matchesMethod = filterMethod === 'all' || paymentMethod.toLowerCase().includes(filterMethod.toLowerCase());
    return matchesSearch && matchesStatus && matchesMethod;
  });

  // Prepare chart data
  const stats = calculateStats();
  const statusData = [
    { name: 'En Attente', value: stats.pending, color: '#f59e0b' },
    { name: 'Approuvé', value: stats.approved, color: '#10b981' },
    { name: 'Payé', value: stats.paid, color: '#3b82f6' }
  ];

  // Method distribution
  const methodCounts = {};
  payouts.forEach(p => {
    const method = (p.payment_method || p.method || 'N/A').replace('_', ' ');
    methodCounts[method] = (methodCounts[method] || 0) + 1;
  });
  const methodData = Object.entries(methodCounts).map(([name, value]) => ({ name, value }));

  // Monthly trend (last 6 months)
  const monthlyData = [];
  const now = new Date();
  for (let i = 5; i >= 0; i--) {
    const month = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const monthName = month.toLocaleDateString('fr-FR', { month: 'short' });
    const monthPayouts = payouts.filter(p => {
      const date = new Date(p.created_at || p.requested_at);
      return date.getMonth() === month.getMonth() && date.getFullYear() === month.getFullYear();
    });
    const amount = monthPayouts.reduce((sum, p) => sum + (parseFloat(p.amount) || 0), 0);
    monthlyData.push({ month: monthName, montant: amount });
  }

  const uniqueMethods = ['all', ...new Set(payouts.map(p => p.payment_method || p.method || 'N/A'))];

  const columns = [
    {
      header: 'Affilié',
      accessor: 'affiliate_name',
      render: (row) => {
        const name = row.influencers?.full_name || row.influencers?.username || row.affiliate_name || 'N/A';
        const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
        return (
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
              {initials}
            </div>
            <div>
              <div className="font-medium text-gray-900">{name}</div>
              <div className="text-sm text-gray-500 flex items-center gap-1">
                <Mail size={12} />
                {row.influencers?.email || 'N/A'}
              </div>
            </div>
          </div>
        );
      },
    },
    {
      header: 'Montant',
      accessor: 'amount',
      render: (row) => (
        <div className="flex items-center gap-2">
          <DollarSign size={16} className="text-green-600" />
          <span className="font-semibold text-gray-900">{formatCurrency(row.amount)}</span>
        </div>
      ),
    },
    {
      header: 'Méthode',
      accessor: 'method',
      render: (row) => {
        const method = row.payment_method || row.method || 'N/A';
        const displayMethod = method.replace('_', ' ');
        const isPayPal = method.toLowerCase().includes('paypal');
        const isBank = method.toLowerCase().includes('bank') || method.toLowerCase().includes('transfer');
        
        return (
          <div className="flex items-center gap-2">
            <CreditCard size={16} className={isPayPal ? 'text-blue-600' : isBank ? 'text-purple-600' : 'text-gray-400'} />
            <span className="capitalize">{displayMethod}</span>
          </div>
        );
      },
    },
    {
      header: 'Statut',
      accessor: 'status',
      render: (row) => {
        const statusConfig = {
          pending: { icon: Clock, color: 'text-orange-600', bg: 'bg-orange-100', label: 'En Attente' },
          approved: { icon: CheckCircle, color: 'text-green-600', bg: 'bg-green-100', label: 'Approuvé' },
          paid: { icon: CheckCircle, color: 'text-blue-600', bg: 'bg-blue-100', label: 'Payé' },
          rejected: { icon: XCircle, color: 'text-red-600', bg: 'bg-red-100', label: 'Rejeté' }
        };
        const config = statusConfig[row.status] || statusConfig.pending;
        const Icon = config.icon;
        
        return (
          <div className="flex items-center gap-2">
            <Icon size={16} className={config.color} />
            <Badge status={row.status}>{config.label}</Badge>
          </div>
        );
      },
    },
    {
      header: 'Demandé le',
      accessor: 'requested_at',
      render: (row) => {
        const date = row.created_at || row.requested_at;
        return (
          <div className="flex items-center gap-2 text-gray-600">
            <Calendar size={14} />
            <span>{date ? formatDate(date) : 'N/A'}</span>
          </div>
        );
      },
    },
    {
      header: 'Traité le',
      accessor: 'processed_at',
      render: (row) => {
        const date = row.paid_at || row.processed_at;
        return date ? (
          <div className="flex items-center gap-2 text-gray-600">
            <Calendar size={14} />
            <span>{formatDate(date)}</span>
          </div>
        ) : (
          <span className="text-gray-400">-</span>
        );
      },
    },
    {
      header: 'Actions',
      accessor: 'actions',
      render: (row) => (
        <div className="flex items-center gap-2">
          <Button 
            size="sm" 
            variant="secondary"
            onClick={() => handleViewDetails(row)}
            className="flex items-center gap-1"
          >
            <Eye size={14} />
          </Button>
          {row.status === 'pending' && (
            <>
              <Button 
                size="sm" 
                variant="success" 
                disabled={loading} 
                onClick={() => handleApprove(row.id)}
                className="flex items-center gap-1"
              >
                <Check size={14} />
              </Button>
              <Button 
                size="sm" 
                variant="danger" 
                disabled={loading} 
                onClick={() => handleReject(row.id)}
                className="flex items-center gap-1"
              >
                <X size={14} />
              </Button>
            </>
          )}
        </div>
      ),
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement des paiements...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6" data-testid="affiliate-payouts">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg">
              <DollarSign className="text-white" size={28} />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Paiements Affiliés</h1>
              <p className="text-gray-600 mt-1">Gérez les demandes de paiement</p>
            </div>
          </div>
        </div>
      </div>

      {/* Animated KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Payouts */}
        <div 
          className={`bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white transform transition-all duration-300 cursor-pointer ${
            hoveredCard === 'total' ? 'scale-105 shadow-2xl' : ''
          }`}
          onMouseEnter={() => setHoveredCard('total')}
          onMouseLeave={() => setHoveredCard(null)}
        >
          <div className="flex items-center justify-between mb-4">
            <DollarSign size={32} className="opacity-80" />
            <div className="text-right">
              <div className="text-3xl font-bold">{animatedValues.total}</div>
              <div className="text-blue-100 text-sm">Total Demandes</div>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <TrendingUp size={16} />
            <span className="font-semibold">{formatCurrency(stats.totalAmount)}</span>
          </div>
        </div>

        {/* Pending */}
        <div 
          className={`bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl shadow-lg p-6 text-white transform transition-all duration-300 cursor-pointer ${
            hoveredCard === 'pending' ? 'scale-105 shadow-2xl' : ''
          }`}
          onMouseEnter={() => setHoveredCard('pending')}
          onMouseLeave={() => setHoveredCard(null)}
        >
          <div className="flex items-center justify-between mb-4">
            <Clock size={32} className="opacity-80" />
            <div className="text-right">
              <div className="text-3xl font-bold">{animatedValues.pending}</div>
              <div className="text-orange-100 text-sm">En Attente</div>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <DollarSign size={16} />
            <span className="font-semibold">{formatCurrency(stats.pendingAmount)}</span>
          </div>
        </div>

        {/* Approved */}
        <div 
          className={`bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-6 text-white transform transition-all duration-300 cursor-pointer ${
            hoveredCard === 'approved' ? 'scale-105 shadow-2xl' : ''
          }`}
          onMouseEnter={() => setHoveredCard('approved')}
          onMouseLeave={() => setHoveredCard(null)}
        >
          <div className="flex items-center justify-between mb-4">
            <CheckCircle size={32} className="opacity-80" />
            <div className="text-right">
              <div className="text-3xl font-bold">{animatedValues.approved}</div>
              <div className="text-green-100 text-sm">Approuvés</div>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Users size={16} />
            <span className="font-semibold">{stats.approved} demandes</span>
          </div>
        </div>

        {/* Paid */}
        <div 
          className={`bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white transform transition-all duration-300 cursor-pointer ${
            hoveredCard === 'paid' ? 'scale-105 shadow-2xl' : ''
          }`}
          onMouseEnter={() => setHoveredCard('paid')}
          onMouseLeave={() => setHoveredCard(null)}
        >
          <div className="flex items-center justify-between mb-4">
            <CheckCircle size={32} className="opacity-80" />
            <div className="text-right">
              <div className="text-3xl font-bold">{animatedValues.paid}</div>
              <div className="text-purple-100 text-sm">Payés</div>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <DollarSign size={16} />
            <span className="font-semibold">{formatCurrency(stats.paidAmount)}</span>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Trend Chart */}
        <Card>
          <div className="p-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <TrendingUp size={20} className="text-blue-600" />
              Tendance Mensuelle
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={monthlyData}>
                <defs>
                  <linearGradient id="colorAmount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="month" stroke="#6b7280" style={{ fontSize: '12px' }} />
                <YAxis stroke="#6b7280" style={{ fontSize: '12px' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                  formatter={(value) => [`${value.toFixed(2)} €`, 'Montant']}
                />
                <Area type="monotone" dataKey="montant" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorAmount)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Status Distribution */}
        <Card>
          <div className="p-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Filter size={20} className="text-purple-600" />
              Distribution par Statut
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={statusData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Payment Methods Distribution */}
        <Card>
          <div className="p-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <CreditCard size={20} className="text-green-600" />
              Méthodes de Paiement
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={methodData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="name" stroke="#6b7280" style={{ fontSize: '12px' }} />
                <YAxis stroke="#6b7280" style={{ fontSize: '12px' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                  formatter={(value) => [value, 'Paiements']}
                />
                <Bar dataKey="value" fill="#10b981" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <div className="p-4 border-b border-gray-200">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Rechercher un affilié..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Status Filter */}
            <div className="w-full md:w-48">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">Tous les statuts</option>
                <option value="pending">En Attente</option>
                <option value="approved">Approuvé</option>
                <option value="paid">Payé</option>
                <option value="rejected">Rejeté</option>
              </select>
            </div>

            {/* Method Filter */}
            <div className="w-full md:w-48">
              <select
                value={filterMethod}
                onChange={(e) => setFilterMethod(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">Toutes les méthodes</option>
                {uniqueMethods.filter(m => m !== 'all').map(method => (
                  <option key={method} value={method}>{method}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          {filteredPayouts.length === 0 ? (
            <div className="text-center py-12">
              <DollarSign size={48} className="mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {searchTerm || filterStatus !== 'all' || filterMethod !== 'all' 
                  ? 'Aucun paiement trouvé' 
                  : 'Aucun paiement'}
              </h3>
              <p className="text-gray-600">
                {searchTerm || filterStatus !== 'all' || filterMethod !== 'all'
                  ? 'Essayez de modifier vos filtres de recherche'
                  : 'Les demandes de paiement apparaîtront ici'}
              </p>
            </div>
          ) : (
            <Table columns={columns} data={filteredPayouts} />
          )}
        </div>
      </Card>

      {/* Details Modal */}
      {showDetails && selectedPayout && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={() => setShowDetails(false)}>
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="p-6">
              {/* Header */}
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Détails du Paiement</h2>
                <button 
                  onClick={() => setShowDetails(false)}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <X size={24} className="text-gray-600" />
                </button>
              </div>

              {/* Profile Section */}
              <div className="flex items-center gap-4 mb-6 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center text-white font-bold text-2xl">
                  {(selectedPayout.influencers?.full_name || selectedPayout.affiliate_name || 'N/A').split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)}
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-900">
                    {selectedPayout.influencers?.full_name || selectedPayout.influencers?.username || selectedPayout.affiliate_name || 'N/A'}
                  </h3>
                  <p className="text-gray-600 flex items-center gap-2">
                    <Mail size={16} />
                    {selectedPayout.influencers?.email || 'N/A'}
                  </p>
                </div>
              </div>

              {/* Payment Details Grid */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="p-4 bg-blue-50 rounded-xl">
                  <div className="flex items-center gap-2 text-blue-600 mb-2">
                    <DollarSign size={20} />
                    <span className="text-sm font-medium">Montant</span>
                  </div>
                  <div className="text-2xl font-bold text-gray-900">{formatCurrency(selectedPayout.amount)}</div>
                </div>

                <div className="p-4 bg-green-50 rounded-xl">
                  <div className="flex items-center gap-2 text-green-600 mb-2">
                    <CreditCard size={20} />
                    <span className="text-sm font-medium">Méthode</span>
                  </div>
                  <div className="text-lg font-semibold text-gray-900 capitalize">
                    {(selectedPayout.payment_method || selectedPayout.method || 'N/A').replace('_', ' ')}
                  </div>
                </div>

                <div className="p-4 bg-purple-50 rounded-xl">
                  <div className="flex items-center gap-2 text-purple-600 mb-2">
                    <Clock size={20} />
                    <span className="text-sm font-medium">Statut</span>
                  </div>
                  <Badge status={selectedPayout.status} className="text-sm">
                    {selectedPayout.status === 'pending' ? 'En Attente' : 
                     selectedPayout.status === 'approved' ? 'Approuvé' : 
                     selectedPayout.status === 'paid' ? 'Payé' : 'Rejeté'}
                  </Badge>
                </div>

                <div className="p-4 bg-orange-50 rounded-xl">
                  <div className="flex items-center gap-2 text-orange-600 mb-2">
                    <Calendar size={20} />
                    <span className="text-sm font-medium">Demandé le</span>
                  </div>
                  <div className="text-sm font-medium text-gray-900">
                    {formatDate(selectedPayout.created_at || selectedPayout.requested_at)}
                  </div>
                </div>
              </div>

              {/* Processing Date */}
              {(selectedPayout.paid_at || selectedPayout.processed_at) && (
                <div className="mb-6 p-4 bg-gray-50 rounded-xl">
                  <div className="flex items-center gap-2 text-gray-600 mb-1">
                    <Calendar size={16} />
                    <span className="text-sm font-medium">Traité le</span>
                  </div>
                  <div className="text-gray-900 font-medium">
                    {formatDate(selectedPayout.paid_at || selectedPayout.processed_at)}
                  </div>
                </div>
              )}

              {/* Actions */}
              {selectedPayout.status === 'pending' && (
                <div className="flex gap-3 pt-4 border-t border-gray-200">
                  <Button
                    variant="success"
                    onClick={() => handleApprove(selectedPayout.id)}
                    className="flex-1 flex items-center justify-center gap-2 py-3"
                  >
                    <CheckCircle size={20} />
                    Approuver le Paiement
                  </Button>
                  <Button
                    variant="danger"
                    onClick={() => handleReject(selectedPayout.id)}
                    className="flex-1 flex items-center justify-center gap-2 py-3"
                  >
                    <XCircle size={20} />
                    Rejeter
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AffiliatePayouts;
