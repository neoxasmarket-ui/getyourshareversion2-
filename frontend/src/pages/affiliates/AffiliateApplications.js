import React, { useState, useMemo, useEffect } from 'react';
import Card from '../../components/common/Card';
import Table from '../../components/common/Table';
import Badge from '../../components/common/Badge';
import Button from '../../components/common/Button';
import { formatDate } from '../../utils/helpers';
import { 
  Check, 
  X, 
  Clock,
  UserPlus,
  Filter,
  Search,
  Globe,
  Mail,
  Calendar,
  AlertCircle,
  TrendingUp,
  Users,
  CheckCircle,
  XCircle,
  Eye,
  ExternalLink,
  ArrowUpRight,
  Flag
} from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis } from 'recharts';

const AffiliateApplications = () => {
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterSource, setFilterSource] = useState('all');
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  const [animatedValues, setAnimatedValues] = useState({
    total: 0,
    pending: 0,
    approved: 0,
    rejected: 0
  });
  
  const [applications] = useState([
    {
      id: 'app_1',
      first_name: 'Sophie',
      last_name: 'Laurent',
      email: 'sophie.laurent@example.com',
      country: 'FR',
      traffic_source: 'Instagram',
      website: 'https://sophiestyle.com',
      followers: 45000,
      engagement_rate: 4.2,
      status: 'pending',
      created_at: '2024-03-20T16:45:00Z',
      message: 'Passionnée de mode et lifestyle, je souhaite promouvoir vos produits auprès de mon audience.',
    },
    {
      id: 'app_2',
      first_name: 'Thomas',
      last_name: 'Moreau',
      email: 'thomas.moreau@example.com',
      country: 'FR',
      traffic_source: 'Blog',
      website: 'https://thomastech.blog',
      followers: 12000,
      engagement_rate: 3.8,
      status: 'pending',
      created_at: '2024-03-22T10:30:00Z',
      message: 'Blogueur tech avec une communauté engagée. Spécialisé dans les reviews produits.',
    },
  ]);

  // Animation des compteurs
  useEffect(() => {
    const stats = calculateStats();
    animateValue(0, stats.total, 1500, 'total');
    animateValue(0, stats.pending, 1200, 'pending');
    animateValue(0, stats.approved, 1300, 'approved');
    animateValue(0, stats.rejected, 1400, 'rejected');
  }, [applications]);

  const animateValue = (start, end, duration, key) => {
    const startTime = Date.now();
    const animate = () => {
      const now = Date.now();
      const progress = Math.min((now - startTime) / duration, 1);
      const value = start + (end - start) * progress;
      setAnimatedValues(prev => ({ ...prev, [key]: Math.floor(value) }));
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    requestAnimationFrame(animate);
  };

  const calculateStats = () => {
    return {
      total: applications.length,
      pending: applications.filter(a => a.status === 'pending').length,
      approved: applications.filter(a => a.status === 'approved').length,
      rejected: applications.filter(a => a.status === 'rejected').length,
    };
  };

  const handleApprove = (id) => {
    setLoading(true);
    // Simuler une API call
    setTimeout(() => {
      setLoading(false);
      alert(`Demande ${id} approuvée!`);
    }, 1000);
  };

  const handleReject = (id) => {
    setLoading(true);
    // Simuler une API call
    setTimeout(() => {
      setLoading(false);
      alert(`Demande ${id} rejetée!`);
    }, 1000);
  };

  const handleViewDetails = (application) => {
    setSelectedRequest(application);
    setShowDetails(true);
  };

  const filteredApplications = applications.filter(app => {
    const search = searchTerm.toLowerCase();
    const matchesSearch = (
      app.first_name?.toLowerCase().includes(search) ||
      app.last_name?.toLowerCase().includes(search) ||
      app.email?.toLowerCase().includes(search)
    );
    const matchesStatus = filterStatus === 'all' || app.status === filterStatus;
    const matchesSource = filterSource === 'all' || app.traffic_source === filterSource;
    
    return matchesSearch && matchesStatus && matchesSource;
  });

  const stats = calculateStats();
  
  // Données pour les graphiques
  const statusData = [
    { name: 'En attente', value: stats.pending, color: '#f59e0b' },
    { name: 'Approuvées', value: stats.approved, color: '#10b981' },
    { name: 'Rejetées', value: stats.rejected, color: '#ef4444' }
  ];

  const sourceStats = applications.reduce((acc, app) => {
    acc[app.traffic_source] = (acc[app.traffic_source] || 0) + 1;
    return acc;
  }, {});

  const sourceData = Object.entries(sourceStats).map(([name, value]) => ({
    name,
    value
  }));

  const uniqueSources = [...new Set(applications.map(a => a.traffic_source))];

  const columns = useMemo(() => [
    {
      header: 'Affilié',
      accessor: 'name',
      render: (row) => (
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
            {row.first_name?.[0]}{row.last_name?.[0]}
          </div>
          <div>
            <div className="font-semibold text-gray-900">{row.first_name} {row.last_name}</div>
            <div className="text-xs text-gray-500 flex items-center gap-1">
              <Mail className="h-3 w-3" />
              {row.email}
            </div>
          </div>
        </div>
      ),
    },
    {
      header: 'Pays',
      accessor: 'country',
      render: (row) => (
        <div className="flex items-center gap-2">
          <Flag className="h-4 w-4 text-gray-400" />
          <span className="font-medium">{row.country}</span>
        </div>
      )
    },
    {
      header: 'Source',
      accessor: 'traffic_source',
      render: (row) => (
        <span className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm font-medium">
          {row.traffic_source}
        </span>
      )
    },
    {
      header: 'Audience',
      accessor: 'followers',
      render: (row) => (
        <div>
          <div className="font-semibold text-gray-900">{row.followers?.toLocaleString()} followers</div>
          <div className="text-xs text-green-600">Engagement: {row.engagement_rate}%</div>
        </div>
      )
    },
    {
      header: 'Site Web',
      accessor: 'website',
      render: (row) => (
        <a 
          href={row.website} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="text-blue-600 hover:text-blue-800 text-sm flex items-center gap-1 hover:underline"
        >
          <Globe className="h-4 w-4" />
          Visiter
          <ExternalLink className="h-3 w-3" />
        </a>
      ),
    },
    {
      header: 'Statut',
      accessor: 'status',
      render: (row) => {
        const statusConfig = {
          pending: { icon: Clock, color: 'yellow', label: 'En attente' },
          approved: { icon: CheckCircle, color: 'green', label: 'Approuvé' },
          rejected: { icon: XCircle, color: 'red', label: 'Rejeté' }
        };
        const config = statusConfig[row.status] || statusConfig.pending;
        const Icon = config.icon;
        return (
          <div className="flex items-center gap-2">
            <Icon className={`h-4 w-4 text-${config.color}-500`} />
            <Badge status={row.status}>{config.label}</Badge>
          </div>
        );
      }
    },
    {
      header: 'Date',
      accessor: 'created_at',
      render: (row) => (
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <Calendar className="h-4 w-4" />
          {formatDate(row.created_at)}
        </div>
      )
    },
    {
      header: 'Actions',
      accessor: 'actions',
      render: (row) => (
        <div className="flex space-x-2">
          <button
            onClick={() => handleViewDetails(row)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Voir détails"
          >
            <Eye className="h-4 w-4 text-gray-600" />
          </button>
          {row.status === 'pending' && (
            <>
              <button
                onClick={() => handleApprove(row.id)}
                disabled={loading}
                className="p-2 bg-green-50 hover:bg-green-100 text-green-600 rounded-lg transition-colors disabled:opacity-50"
                title="Approuver"
              >
                <Check className="h-4 w-4" />
              </button>
              <button
                onClick={() => handleReject(row.id)}
                disabled={loading}
                className="p-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg transition-colors disabled:opacity-50"
                title="Rejeter"
              >
                <X className="h-4 w-4" />
              </button>
            </>
          )}
        </div>
      ),
    },
  ], [loading]);

  return (
    <div className="space-y-6" data-testid="affiliate-applications">
      {/* En-tête */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <UserPlus className="h-8 w-8 text-blue-600" />
            Demandes d'Affiliation
          </h1>
          <p className="text-gray-600 mt-2">
            Examinez et validez les nouvelles candidatures
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Filter size={20} className="mr-2" />
            Filtres avancés
          </Button>
        </div>
      </div>

      {/* KPIs animés */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total demandes */}
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg transform hover:scale-105 transition-transform">
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-blue-100 text-sm font-medium">Total Demandes</p>
              <p className="text-3xl font-bold mt-2">{animatedValues.total}</p>
            </div>
            <div className="bg-white/20 p-3 rounded-lg">
              <Users className="h-6 w-6" />
            </div>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <ArrowUpRight className="h-4 w-4" />
            <span>+8 cette semaine</span>
          </div>
        </div>

        {/* En attente */}
        <div className="bg-gradient-to-br from-amber-500 to-orange-600 rounded-xl p-6 text-white shadow-lg transform hover:scale-105 transition-transform">
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-amber-100 text-sm font-medium">En Attente</p>
              <p className="text-3xl font-bold mt-2">{animatedValues.pending}</p>
            </div>
            <div className="bg-white/20 p-3 rounded-lg">
              <Clock className="h-6 w-6" />
            </div>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <AlertCircle className="h-4 w-4" />
            <span>À traiter rapidement</span>
          </div>
        </div>

        {/* Approuvées */}
        <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl p-6 text-white shadow-lg transform hover:scale-105 transition-transform">
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-green-100 text-sm font-medium">Approuvées</p>
              <p className="text-3xl font-bold mt-2">{animatedValues.approved}</p>
            </div>
            <div className="bg-white/20 p-3 rounded-lg">
              <CheckCircle className="h-6 w-6" />
            </div>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <TrendingUp className="h-4 w-4" />
            <span>{stats.total > 0 ? Math.round((stats.approved / stats.total) * 100) : 0}% taux approbation</span>
          </div>
        </div>

        {/* Rejetées */}
        <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-xl p-6 text-white shadow-lg transform hover:scale-105 transition-transform">
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-red-100 text-sm font-medium">Rejetées</p>
              <p className="text-3xl font-bold mt-2">{animatedValues.rejected}</p>
            </div>
            <div className="bg-white/20 p-3 rounded-lg">
              <XCircle className="h-6 w-6" />
            </div>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <span>{stats.total > 0 ? Math.round((stats.rejected / stats.total) * 100) : 0}% taux rejet</span>
          </div>
        </div>
      </div>

      {/* Graphiques */}
      {applications.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Distribution par statut */}
          <Card>
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-blue-600" />
              Distribution par Statut
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={statusData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-2">
              {statusData.map((item, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                    <span className="text-sm text-gray-600">{item.name}</span>
                  </div>
                  <span className="text-sm font-semibold">{item.value}</span>
                </div>
              ))}
            </div>
          </Card>

          {/* Sources de trafic */}
          <Card>
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Globe className="h-5 w-5 text-purple-600" />
              Sources de Trafic
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={sourceData}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </div>
      )}

      {/* Filtres et recherche */}
      <Card>
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Rechercher par nom ou email..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div className="flex gap-2">
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Tous les statuts</option>
              <option value="pending">En attente</option>
              <option value="approved">Approuvées</option>
              <option value="rejected">Rejetées</option>
            </select>
            <select
              value={filterSource}
              onChange={(e) => setFilterSource(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Toutes les sources</option>
              {uniqueSources.map(source => (
                <option key={source} value={source}>{source}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Table */}
        {filteredApplications.length > 0 ? (
          <div className="overflow-x-auto">
            <Table columns={columns} data={filteredApplications} />
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-50 rounded-full mb-4">
              <UserPlus className="h-10 w-10 text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              {applications.length === 0 ? 'Aucune demande' : 'Aucun résultat'}
            </h3>
            <p className="text-gray-500 mb-6 max-w-md mx-auto">
              {applications.length === 0 
                ? "Les demandes d'affiliation apparaîtront ici lorsque des influenceurs souhaitent rejoindre votre programme."
                : 'Aucune demande ne correspond aux critères de recherche. Essayez de modifier vos filtres.'}
            </p>
          </div>
        )}
      </Card>

      {/* Modal de détails */}
      {showDetails && selectedRequest && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-start mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Détails de la demande</h2>
              <button
                onClick={() => setShowDetails(false)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="space-y-6">
              {/* Profil */}
              <div className="flex items-center gap-4">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-3xl">
                  {selectedRequest.first_name?.[0]}{selectedRequest.last_name?.[0]}
                </div>
                <div>
                  <h3 className="text-xl font-semibold">{selectedRequest.first_name} {selectedRequest.last_name}</h3>
                  <p className="text-gray-600">{selectedRequest.email}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <Flag className="h-4 w-4 text-gray-400" />
                    <span className="text-sm text-gray-600">{selectedRequest.country}</span>
                  </div>
                </div>
              </div>

              {/* Statistiques */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-purple-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Source de trafic</p>
                  <p className="text-lg font-semibold text-purple-600">{selectedRequest.traffic_source}</p>
                </div>
                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Site web</p>
                  <a href={selectedRequest.website} target="_blank" rel="noopener noreferrer" className="text-lg font-semibold text-blue-600 hover:underline flex items-center gap-1">
                    Visiter <ExternalLink className="h-4 w-4" />
                  </a>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Followers</p>
                  <p className="text-lg font-semibold text-green-600">{selectedRequest.followers?.toLocaleString()}</p>
                </div>
                <div className="bg-orange-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Engagement</p>
                  <p className="text-lg font-semibold text-orange-600">{selectedRequest.engagement_rate}%</p>
                </div>
              </div>

              {/* Message */}
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Message de motivation</h4>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-gray-700">{selectedRequest.message}</p>
                </div>
              </div>

              {/* Date */}
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Calendar className="h-4 w-4" />
                Demande soumise le {formatDate(selectedRequest.created_at)}
              </div>

              {/* Actions */}
              {selectedRequest.status === 'pending' && (
                <div className="flex gap-3 pt-4 border-t">
                  <button
                    onClick={() => {
                      handleApprove(selectedRequest.id);
                      setShowDetails(false);
                    }}
                    className="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
                  >
                    <Check className="h-5 w-5" />
                    Approuver
                  </button>
                  <button
                    onClick={() => {
                      handleReject(selectedRequest.id);
                      setShowDetails(false);
                    }}
                    className="flex-1 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center justify-center gap-2"
                  >
                    <X className="h-5 w-5" />
                    Rejeter
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AffiliateApplications;
