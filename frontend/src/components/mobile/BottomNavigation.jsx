import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Home, Search, PlusCircle, BarChart2, User,
  Target, Heart, Zap, Award
} from 'lucide-react';

/**
 * Bottom navigation bar for mobile
 * Context-aware based on user type
 */
const BottomNavigation = ({ userType }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(getActiveTab(location.pathname));

  function getActiveTab(pathname) {
    if (pathname.includes('/dashboard') || pathname === '/') return 'home';
    if (pathname.includes('/matching') || pathname.includes('/search')) return 'search';
    if (pathname.includes('/analytics')) return 'analytics';
    if (pathname.includes('/profile') || pathname.includes('/gamification')) return 'profile';
    return 'home';
  }

  const getNavItems = () => {
    if (userType === 'merchant') {
      return [
        {
          id: 'home',
          icon: Home,
          label: 'Accueil',
          path: '/dashboard'
        },
        {
          id: 'search',
          icon: Search,
          label: 'Influenceurs',
          path: '/influencer-matching'
        },
        {
          id: 'add',
          icon: PlusCircle,
          label: 'Produit',
          path: '/products/new',
          highlighted: true
        },
        {
          id: 'analytics',
          icon: BarChart2,
          label: 'Analytics',
          path: '/analytics-pro'
        },
        {
          id: 'profile',
          icon: User,
          label: 'Profil',
          path: '/profile'
        }
      ];
    } else if (userType === 'influencer') {
      return [
        {
          id: 'home',
          icon: Home,
          label: 'Accueil',
          path: '/dashboard'
        },
        {
          id: 'search',
          icon: Heart,
          label: 'Marques',
          path: '/brands'
        },
        {
          id: 'add',
          icon: Zap,
          label: 'Contenu',
          path: '/content/new',
          highlighted: true
        },
        {
          id: 'analytics',
          icon: BarChart2,
          label: 'Stats',
          path: '/analytics-pro'
        },
        {
          id: 'profile',
          icon: Award,
          label: 'Niveaux',
          path: '/gamification'
        }
      ];
    } else {
      // Sales Rep
      return [
        {
          id: 'home',
          icon: Home,
          label: 'Accueil',
          path: '/sales/dashboard'
        },
        {
          id: 'search',
          icon: Target,
          label: 'Leads',
          path: '/sales/leads'
        },
        {
          id: 'add',
          icon: PlusCircle,
          label: 'Nouveau',
          path: '/sales/leads/new',
          highlighted: true
        },
        {
          id: 'analytics',
          icon: BarChart2,
          label: 'Pipeline',
          path: '/sales/pipeline'
        },
        {
          id: 'profile',
          icon: User,
          label: 'Profil',
          path: '/profile'
        }
      ];
    }
  };

  const navItems = getNavItems();

  const handleNavigation = (item) => {
    setActiveTab(item.id);
    navigate(item.path);

    // Haptic feedback on mobile
    if ('vibrate' in navigator) {
      navigator.vibrate(10);
    }
  };

  return (
    <nav 
      className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50"
      role="navigation"
      aria-label="Navigation mobile principale"
    >
      <div className="flex items-center justify-around px-2 py-2 max-w-screen-sm mx-auto">
        {navItems.map((item) => (
          <NavItem
            key={item.id}
            item={item}
            isActive={activeTab === item.id}
            onClick={() => handleNavigation(item)}
          />
        ))}
      </div>

      {/* Safe area for iOS notch */}
      <div className="h-safe-area-inset-bottom bg-white"></div>
    </nav>
  );
};

const NavItem = ({ item, isActive, onClick }) => {
  const Icon = item.icon;

  if (item.highlighted) {
    // Center floating action button
    // ✅ FIX ACCESSIBILITÉ P1: Touch target 48x48px minimum + aria-label
    return (
      <button
        onClick={onClick}
        aria-label={item.label}
        className="relative -mt-8 active:scale-95 transition min-w-[48px] min-h-[48px]"
      >
        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-xl">
          <Icon className="h-7 w-7 text-white" aria-hidden="true" />
        </div>
      </button>
    );
  }

  return (
    <button
      onClick={onClick}
      aria-label={item.label}
      aria-current={isActive ? 'page' : undefined}
      className={`flex flex-col items-center justify-center py-2 px-3 rounded-xl transition min-w-[48px] min-h-[48px] ${
        isActive
          ? 'text-blue-600'
          : 'text-gray-500 hover:text-gray-700 active:bg-gray-100'
      }`}
    >
      <Icon 
        className={`h-6 w-6 mb-1 ${isActive ? 'stroke-2' : 'stroke-1.5'}`} 
        aria-hidden="true"
      />
      <span className={`text-xs font-medium ${isActive ? 'font-semibold' : ''}`}>
        {item.label}
      </span>
      {isActive && (
        <div className="absolute bottom-0 w-1 h-1 bg-blue-600 rounded-full" aria-hidden="true"></div>
      )}
    </button>
  );
};

export default BottomNavigation;
