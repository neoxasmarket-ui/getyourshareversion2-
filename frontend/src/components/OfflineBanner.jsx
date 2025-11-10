/**
 * OfflineBanner Component
 * Banner élégant pour indiquer le mode hors ligne
 * Avec animations et auto-hide quand online
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { WifiOff, Wifi, Cloud, CloudOff, RefreshCw } from 'lucide-react';
import useOfflineStatus from '../hooks/useOfflineStatus';

const OfflineBanner = () => {
  const {
    isOnline,
    isOffline,
    wasOffline,
    queuedCount,
    isSyncing,
    connectionType,
    syncQueuedRequests,
  } = useOfflineStatus();

  const [showBanner, setShowBanner] = useState(false);
  const [autoHideTimer, setAutoHideTimer] = useState(null);

  /**
   * Afficher/cacher le banner selon l'état de connexion
   */
  useEffect(() => {
    if (isOffline) {
      setShowBanner(true);
      // Annuler le timer de masquage automatique
      if (autoHideTimer) {
        clearTimeout(autoHideTimer);
        setAutoHideTimer(null);
      }
    } else if (wasOffline && isOnline) {
      // Afficher brièvement le message "Connexion rétablie"
      setShowBanner(true);

      // Auto-hide après 5 secondes
      const timer = setTimeout(() => {
        setShowBanner(false);
      }, 5000);

      setAutoHideTimer(timer);
    } else {
      setShowBanner(false);
    }

    return () => {
      if (autoHideTimer) {
        clearTimeout(autoHideTimer);
      }
    };
  }, [isOffline, wasOffline, isOnline]);

  /**
   * Fermer le banner manuellement
   */
  const handleClose = () => {
    setShowBanner(false);
  };

  /**
   * Synchroniser manuellement
   */
  const handleSync = async () => {
    await syncQueuedRequests();
  };

  return (
    <AnimatePresence>
      {showBanner && (
        <motion.div
          initial={{ y: -100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: -100, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          className={`fixed top-0 left-0 right-0 z-50 ${
            isOffline
              ? 'bg-gradient-to-r from-orange-500 to-red-500'
              : 'bg-gradient-to-r from-green-500 to-emerald-500'
          } text-white shadow-lg`}
        >
          <div className="container mx-auto px-4 py-3">
            <div className="flex items-center justify-between">
              {/* Left: Status Icon & Message */}
              <div className="flex items-center space-x-3">
                {isOffline ? (
                  <>
                    <motion.div
                      animate={{ rotate: [0, 10, -10, 0] }}
                      transition={{ repeat: Infinity, duration: 2 }}
                    >
                      <WifiOff className="w-6 h-6" />
                    </motion.div>
                    <div>
                      <p className="font-semibold text-sm">Mode Hors Ligne</p>
                      <p className="text-xs opacity-90">
                        Certaines fonctionnalités sont limitées
                      </p>
                    </div>
                  </>
                ) : (
                  <>
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: 'spring', stiffness: 500 }}
                    >
                      <Wifi className="w-6 h-6" />
                    </motion.div>
                    <div>
                      <p className="font-semibold text-sm">Connexion Rétablie</p>
                      <p className="text-xs opacity-90">
                        {connectionType !== 'unknown' ? `Connexion ${connectionType}` : 'En ligne'}
                      </p>
                    </div>
                  </>
                )}
              </div>

              {/* Center: Queued Requests & Sync Status */}
              {queuedCount > 0 && (
                <div className="hidden md:flex items-center space-x-2 bg-white/20 backdrop-blur-sm px-3 py-1.5 rounded-full">
                  {isSyncing ? (
                    <>
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                      >
                        <RefreshCw className="w-4 h-4" />
                      </motion.div>
                      <span className="text-xs font-medium">Synchronisation...</span>
                    </>
                  ) : (
                    <>
                      <CloudOff className="w-4 h-4" />
                      <span className="text-xs font-medium">
                        {queuedCount} requête{queuedCount > 1 ? 's' : ''} en attente
                      </span>
                      {isOnline && (
                        <button
                          onClick={handleSync}
                          className="ml-2 text-xs underline hover:no-underline"
                        >
                          Synchroniser
                        </button>
                      )}
                    </>
                  )}
                </div>
              )}

              {/* Right: Close Button */}
              {isOnline && (
                <button
                  onClick={handleClose}
                  className="text-white/80 hover:text-white transition-colors"
                  aria-label="Fermer"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default OfflineBanner;
