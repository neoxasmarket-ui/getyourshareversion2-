import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import { MessageSquare, AlertTriangle, ShieldAlert, Users, TrendingUp, CheckCircle } from 'lucide-react';

const News = () => {
  const navigate = useNavigate();
  
  const moderationStats = [
    {
      label: 'Conversations actives',
      value: '8',
      icon: MessageSquare,
      color: 'bg-blue-100 text-blue-600',
      trend: '+2 cette semaine'
    },
    {
      label: 'Signalements en attente',
      value: '0',
      icon: AlertTriangle,
      color: 'bg-yellow-100 text-yellow-600',
      trend: 'Aucun nouveau'
    },
    {
      label: 'Litiges résolus',
      value: '12',
      icon: CheckCircle,
      color: 'bg-green-100 text-green-600',
      trend: '+3 ce mois'
    },
    {
      label: 'Utilisateurs actifs',
      value: '45',
      icon: Users,
      color: 'bg-purple-100 text-purple-600',
      trend: '+8% ce mois'
    }
  ];

  const recentActivities = [
    {
      id: 1,
      type: 'conversation',
      title: 'Nouvelle conversation créée',
      description: 'Digital Marketing MA ↔ affiliate_user',
      time: 'Il y a 2 heures',
      icon: MessageSquare,
      color: 'text-blue-600'
    },
    {
      id: 2,
      type: 'resolution',
      title: 'Litige résolu',
      description: 'Problème de paiement résolu entre E-Commerce Plus et influencer_pro',
      time: 'Il y a 5 heures',
      icon: CheckCircle,
      color: 'text-green-600'
    },
    {
      id: 3,
      type: 'alert',
      title: 'Vérification requise',
      description: 'Activité inhabituelle détectée sur le compte TechCorp SAS',
      time: 'Hier',
      icon: ShieldAlert,
      color: 'text-orange-600'
    }
  ];

  return (
    <div className="space-y-6" data-testid="news">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">🛡️ Modération & Support</h1>
        <p className="text-gray-600 mt-2">Gérez les conversations, résolvez les litiges et supervisez la plateforme</p>
      </div>

      {/* Statistiques de modération */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {moderationStats.map((stat, index) => (
          <Card key={index}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                <p className="text-xs text-gray-500 mt-1">{stat.trend}</p>
              </div>
              <div className={`w-12 h-12 rounded-full flex items-center justify-center ${stat.color}`}>
                <stat.icon size={24} />
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Activités récentes */}
        <div className="lg:col-span-2 space-y-4">
          <Card title="Activités récentes">
            <div className="space-y-4">
              {recentActivities.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-4 pb-4 border-b last:border-b-0">
                  <div className={`flex-shrink-0 ${activity.color}`}>
                    <activity.icon size={24} />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{activity.title}</h3>
                    <p className="text-sm text-gray-600 mt-1">{activity.description}</p>
                    <p className="text-xs text-gray-400 mt-2">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Actions rapides */}
        <div className="space-y-4">
          <Card title="Actions rapides">
            <div className="space-y-3">
              <button 
                onClick={() => navigate('/messages')}
                className="w-full text-left px-4 py-3 bg-indigo-50 hover:bg-indigo-100 rounded-lg transition-all flex items-center space-x-3"
              >
                <MessageSquare size={20} className="text-indigo-600" />
                <div>
                  <p className="font-medium text-indigo-900">Voir toutes les conversations</p>
                  <p className="text-xs text-indigo-600">8 conversations actives</p>
                </div>
              </button>
              
              <button 
                className="w-full text-left px-4 py-3 bg-yellow-50 hover:bg-yellow-100 rounded-lg transition-all flex items-center space-x-3"
              >
                <AlertTriangle size={20} className="text-yellow-600" />
                <div>
                  <p className="font-medium text-yellow-900">Signalements</p>
                  <p className="text-xs text-yellow-600">0 en attente</p>
                </div>
              </button>
              
              <button 
                onClick={() => navigate('/users')}
                className="w-full text-left px-4 py-3 bg-purple-50 hover:bg-purple-100 rounded-lg transition-all flex items-center space-x-3"
              >
                <Users size={20} className="text-purple-600" />
                <div>
                  <p className="font-medium text-purple-900">Gérer les utilisateurs</p>
                  <p className="text-xs text-purple-600">45 utilisateurs actifs</p>
                </div>
              </button>
              
              <button 
                className="w-full text-left px-4 py-3 bg-green-50 hover:bg-green-100 rounded-lg transition-all flex items-center space-x-3"
              >
                <TrendingUp size={20} className="text-green-600" />
                <div>
                  <p className="font-medium text-green-900">Statistiques</p>
                  <p className="text-xs text-green-600">Voir les rapports</p>
                </div>
              </button>
            </div>
          </Card>

          <Card title="💡 Conseil">
            <p className="text-sm text-gray-600">
              Consultez régulièrement les conversations pour identifier les problèmes avant qu'ils ne s'aggravent. 
              Une intervention rapide améliore la satisfaction des utilisateurs.
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default News;
