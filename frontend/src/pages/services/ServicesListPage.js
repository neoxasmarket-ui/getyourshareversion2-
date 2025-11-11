import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import api from '../../utils/api';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Table from '../../components/common/Table';
import Modal from '../../components/common/Modal';
import Badge from '../../components/common/Badge';
import EmptyState from '../../components/common/EmptyState';
import {
  Briefcase, Plus, Edit, Trash2, Search, Eye, TrendingUp,
  DollarSign, Archive, Users
} from 'lucide-react';

const ServicesListPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const toast = useToast();
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, service: null });
  const [stats, setStats] = useState({
    total: 0,
    active: 0,
    avgPricePerLead: 0,
    totalCapacity: 0
  });

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/services');
      const servicesData = response.data.services || [];
      setServices(servicesData);
      
      // Calculer statistiques
      const total = servicesData.length;
      const active = servicesData.filter(s => s.is_available !== false).length;
      const avgPricePerLead = total > 0 
        ? servicesData.reduce((sum, s) => sum + (parseFloat(s.price_per_lead) || 0), 0) / total
        : 0;
      const totalCapacity = servicesData.reduce((sum, s) => sum + (parseInt(s.capacity_per_month) || 0), 0);
      
      setStats({ total, active, avgPricePerLead, totalCapacity });
    } catch (error) {
      console.error('Error fetching services:', error);
      toast.error('Erreur lors du chargement des services');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (serviceId) => {
    try {
      await api.delete(`/api/services/${serviceId}`);
      setDeleteModal({ isOpen: false, service: null });
      await fetchServices();
      toast.success('Service supprimé avec succès');
    } catch (error) {
      console.error('Error deleting service:', error);
      toast.error('Erreur lors de la suppression du service');
    }
  };

  const filteredServices = services.filter(service =>
    service.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    service.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    service.category?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Fonction utilitaire pour gérer les images (JSONB array)
  const getFirstImage = (service) => {
    if (!service.images) return null;

    if (Array.isArray(service.images) && service.images.length > 0) {
      return service.images[0];
    }

    if (typeof service.images === 'string') {
      try {
        const parsed = JSON.parse(service.images);
        return Array.isArray(parsed) && parsed.length > 0 ? parsed[0] : null;
      } catch {
        return null;
      }
    }

    return null;
  };

  const columns = useMemo(() => [
    {
      key: 'name',
      label: 'Service',
      render: (service) => {
        const imageUrl = getFirstImage(service);
        
        return (
          <div className="flex items-center space-x-3">
            {imageUrl ? (
              <img 
                src={imageUrl} 
                alt={service.name}
                className="w-12 h-12 rounded-lg object-cover"
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            ) : (
              <div className="w-12 h-12 bg-gradient-to-br from-teal-100 to-teal-200 rounded-lg flex items-center justify-center">
                <Briefcase className="text-teal-600" size={24} />
              </div>
            )}
            <div>
              <div className="font-medium text-gray-900">{service.name}</div>
              <div className="text-sm text-gray-500">{service.category}</div>
            </div>
          </div>
        );
      }
    },
    {
      key: 'merchant',
      label: 'Marchand',
      render: (service) => (
        <div className="text-sm">
          <div className="font-medium text-gray-900">
            {service.merchant?.company_name || 'N/A'}
          </div>
          <div className="text-gray-500">
            {service.merchant?.email || ''}
          </div>
        </div>
      )
    },
    {
      key: 'price_per_lead',
      label: 'Prix/Lead',
      render: (service) => (
        <div className="font-medium text-teal-600">
          {parseFloat(service.price_per_lead || 0).toFixed(2)} €
        </div>
      )
    },
    {
      key: 'capacity_per_month',
      label: 'Capacité/Mois',
      render: (service) => (
        <div className="text-sm">
          <div className="flex items-center space-x-1">
            <Users size={14} className="text-gray-400" />
            <span>{service.capacity_per_month || 0} leads</span>
          </div>
          <div className="text-xs text-gray-500">
            {service.total_leads || 0} utilisés
          </div>
        </div>
      )
    },
    {
      key: 'status',
      label: 'Statut',
      render: (service) => (
        <Badge
          variant={service.is_available !== false ? 'success' : 'secondary'}
          text={service.is_available !== false ? 'Disponible' : 'Indisponible'}
        />
      )
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (service) => (
        <div className="flex items-center space-x-2">
          <button
            onClick={() => navigate(`/services/${service.id}`)}
            className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
            title="Voir détails"
          >
            <Eye size={18} />
          </button>
          <button
            onClick={() => navigate(`/services/${service.id}/edit`)}
            className="p-2 text-yellow-600 hover:bg-yellow-50 rounded-lg transition-colors"
            title="Modifier"
          >
            <Edit size={18} />
          </button>
          <button
            onClick={() => setDeleteModal({ isOpen: true, service })}
            className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Supprimer"
          >
            <Trash2 size={18} />
          </button>
        </div>
      )
    }
  ], [navigate]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement des services...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Services</h1>
          <p className="mt-1 text-gray-600">
            Gérez tous les services de la plateforme
          </p>
        </div>
        <Button
          onClick={() => navigate('/services/create')}
          icon={<Plus size={20} />}
        >
          Nouveau Service
        </Button>
      </div>

      {/* Cartes de statistiques */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Services</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{stats.total}</p>
            </div>
            <div className="p-3 bg-teal-100 rounded-lg">
              <Briefcase className="text-teal-600" size={24} />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Services Actifs</p>
              <p className="text-2xl font-bold text-green-600 mt-1">{stats.active}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <TrendingUp className="text-green-600" size={24} />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Prix Moyen/Lead</p>
              <p className="text-2xl font-bold text-blue-600 mt-1">
                {stats.avgPricePerLead.toFixed(2)} €
              </p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <DollarSign className="text-blue-600" size={24} />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Capacité Totale</p>
              <p className="text-2xl font-bold text-purple-600 mt-1">
                {stats.totalCapacity} leads/mois
              </p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <Users className="text-purple-600" size={24} />
            </div>
          </div>
        </Card>
      </div>

      {/* Barre de recherche et filtres */}
      <Card>
        <div className="p-6">
          <div className="flex items-center space-x-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Rechercher un service..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        {/* Tableau des services */}
        {filteredServices.length === 0 ? (
          <EmptyState
            icon={<Briefcase size={48} />}
            title="Aucun service trouvé"
            description={searchTerm ? "Aucun service ne correspond à votre recherche" : "Commencez par créer votre premier service"}
            action={
              !searchTerm && (
                <Button
                  onClick={() => navigate('/services/create')}
                  icon={<Plus size={20} />}
                >
                  Créer un service
                </Button>
              )
            }
          />
        ) : (
          <Table
            data={filteredServices}
            columns={columns}
          />
        )}
      </Card>

      {/* Modal de confirmation de suppression */}
      <Modal
        isOpen={deleteModal.isOpen}
        onClose={() => setDeleteModal({ isOpen: false, service: null })}
        title="Supprimer le service"
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            Êtes-vous sûr de vouloir supprimer le service <strong>{deleteModal.service?.name}</strong> ? 
            Cette action est irréversible.
          </p>
          <div className="flex justify-end space-x-3">
            <Button
              variant="secondary"
              onClick={() => setDeleteModal({ isOpen: false, service: null })}
            >
              Annuler
            </Button>
            <Button
              variant="danger"
              onClick={() => handleDelete(deleteModal.service?.id)}
              icon={<Trash2 size={18} />}
            >
              Supprimer
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default ServicesListPage;
