/**
 * IndexedDB Wrapper
 * Gestion du stockage offline pour la PWA
 * CRUD operations, Sync queue management, Cache invalidation
 */

// Configuration
const DB_NAME = 'ShareYourSales-Offline';
const DB_VERSION = 1;

// Object Stores
const STORES = {
  CACHE: 'cache',
  SYNC_QUEUE: 'sync-queue',
  USER_DATA: 'user-data',
  PRODUCTS: 'products',
  ANALYTICS: 'analytics',
  SETTINGS: 'settings',
};

// Cache TTL (Time To Live) en millisecondes
const CACHE_TTL = {
  SHORT: 5 * 60 * 1000, // 5 minutes
  MEDIUM: 30 * 60 * 1000, // 30 minutes
  LONG: 24 * 60 * 60 * 1000, // 24 heures
  PERMANENT: Infinity,
};

/**
 * Ouvrir la base de données IndexedDB
 */
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onerror = () => {
      console.error('❌ Erreur ouverture IndexedDB:', request.error);
      reject(request.error);
    };

    request.onsuccess = () => {
      resolve(request.result);
    };

    request.onupgradeneeded = (event) => {
      const db = event.target.result;

      // Créer les object stores si nécessaire
      if (!db.objectStoreNames.contains(STORES.CACHE)) {
        const cacheStore = db.createObjectStore(STORES.CACHE, { keyPath: 'key' });
        cacheStore.createIndex('timestamp', 'timestamp', { unique: false });
        cacheStore.createIndex('ttl', 'ttl', { unique: false });
      }

      if (!db.objectStoreNames.contains(STORES.SYNC_QUEUE)) {
        const syncStore = db.createObjectStore(STORES.SYNC_QUEUE, { keyPath: 'id', autoIncrement: true });
        syncStore.createIndex('timestamp', 'timestamp', { unique: false });
        syncStore.createIndex('status', 'status', { unique: false });
      }

      if (!db.objectStoreNames.contains(STORES.USER_DATA)) {
        db.createObjectStore(STORES.USER_DATA, { keyPath: 'userId' });
      }

      if (!db.objectStoreNames.contains(STORES.PRODUCTS)) {
        const productStore = db.createObjectStore(STORES.PRODUCTS, { keyPath: 'id' });
        productStore.createIndex('category', 'category', { unique: false });
        productStore.createIndex('merchant', 'merchant', { unique: false });
      }

      if (!db.objectStoreNames.contains(STORES.ANALYTICS)) {
        const analyticsStore = db.createObjectStore(STORES.ANALYTICS, { keyPath: 'id', autoIncrement: true });
        analyticsStore.createIndex('timestamp', 'timestamp', { unique: false });
        analyticsStore.createIndex('event', 'event', { unique: false });
      }

      if (!db.objectStoreNames.contains(STORES.SETTINGS)) {
        db.createObjectStore(STORES.SETTINGS, { keyPath: 'key' });
      }

      console.log('✅ IndexedDB initialisée avec succès');
    };
  });
}

/**
 * CACHE OPERATIONS
 */

// Ajouter/Mettre à jour dans le cache
export async function setCache(key, value, ttl = CACHE_TTL.MEDIUM) {
  try {
    const db = await openDB();
    const transaction = db.transaction([STORES.CACHE], 'readwrite');
    const store = transaction.objectStore(STORES.CACHE);

    const cacheItem = {
      key,
      value,
      timestamp: Date.now(),
      ttl,
      expiresAt: ttl === Infinity ? Infinity : Date.now() + ttl,
    };

    await new Promise((resolve, reject) => {
      const request = store.put(cacheItem);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    console.log(`✅ Cache set: ${key}`);
    return true;
  } catch (error) {
    console.error('❌ Erreur setCache:', error);
    return false;
  }
}

// Récupérer du cache
export async function getCache(key, ignoreExpiration = false) {
  try {
    const db = await openDB();
    const transaction = db.transaction([STORES.CACHE], 'readonly');
    const store = transaction.objectStore(STORES.CACHE);

    const cacheItem = await new Promise((resolve, reject) => {
      const request = store.get(key);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    if (!cacheItem) {
      return null;
    }

    // Vérifier l'expiration
    if (!ignoreExpiration && cacheItem.expiresAt !== Infinity && Date.now() > cacheItem.expiresAt) {
      console.log(`⏰ Cache expiré: ${key}`);
      await deleteCache(key);
      return null;
    }

    console.log(`✅ Cache hit: ${key}`);
    return cacheItem.value;
  } catch (error) {
    console.error('❌ Erreur getCache:', error);
    return null;
  }
}

// Supprimer du cache
export async function deleteCache(key) {
  try {
    const db = await openDB();
    const transaction = db.transaction([STORES.CACHE], 'readwrite');
    const store = transaction.objectStore(STORES.CACHE);

    await new Promise((resolve, reject) => {
      const request = store.delete(key);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });

    console.log(`🗑️ Cache deleted: ${key}`);
    return true;
  } catch (error) {
    console.error('❌ Erreur deleteCache:', error);
    return false;
  }
}

// Vider tout le cache
export async function clearCache() {
  try {
    const db = await openDB();
    const transaction = db.transaction([STORES.CACHE], 'readwrite');
    const store = transaction.objectStore(STORES.CACHE);

    await new Promise((resolve, reject) => {
      const request = store.clear();
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });

    console.log('🗑️ Cache entièrement vidé');
    return true;
  } catch (error) {
    console.error('❌ Erreur clearCache:', error);
    return false;
  }
}

// Nettoyer le cache expiré
export async function cleanExpiredCache() {
  try {
    const db = await openDB();
    const transaction = db.transaction([STORES.CACHE], 'readwrite');
    const store = transaction.objectStore(STORES.CACHE);

    const allItems = await new Promise((resolve, reject) => {
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    let deletedCount = 0;
    const now = Date.now();

    for (const item of allItems) {
      if (item.expiresAt !== Infinity && now > item.expiresAt) {
        await deleteCache(item.key);
        deletedCount++;
      }
    }

    console.log(`🧹 ${deletedCount} entrées expirées supprimées`);
    return deletedCount;
  } catch (error) {
    console.error('❌ Erreur cleanExpiredCache:', error);
    return 0;
  }
}

/**
 * SYNC QUEUE OPERATIONS
 */

// Ajouter à la file de synchronisation
export async function addToSyncQueue(url, method, data, options = {}) {
  try {
    const db = await openDB();
    const transaction = db.transaction([STORES.SYNC_QUEUE], 'readwrite');
    const store = transaction.objectStore(STORES.SYNC_QUEUE);

    const queueItem = {
      url,
      method: method || 'POST',
      data,
      options,
      timestamp: Date.now(),
      status: 'pending',
      retryCount: 0,
    };

    const id = await new Promise((resolve, reject) => {
      const request = store.add(queueItem);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    console.log(`📥 Ajouté à la queue de sync: ${url} (ID: ${id})`);
    return id;
  } catch (error) {
    console.error('❌ Erreur addToSyncQueue:', error);
    return null;
  }
}

// Récupérer toutes les requêtes en attente
export async function getSyncQueue(status = 'pending') {
  try {
    const db = await openDB();
    const transaction = db.transaction([STORES.SYNC_QUEUE], 'readonly');
    const store = transaction.objectStore(STORES.SYNC_QUEUE);
    const index = store.index('status');

    const queue = await new Promise((resolve, reject) => {
      const request = index.getAll(status);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    return queue;
  } catch (error) {
    console.error('❌ Erreur getSyncQueue:', error);
    return [];
  }
}

// Mettre à jour le statut d'une requête
export async function updateSyncQueueItem(id, updates) {
  try {
    const db = await openDB();
    const transaction = db.transaction([STORES.SYNC_QUEUE], 'readwrite');
    const store = transaction.objectStore(STORES.SYNC_QUEUE);

    const item = await new Promise((resolve, reject) => {
      const request = store.get(id);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    if (!item) {
      throw new Error(`Item ${id} non trouvé`);
    }

    const updatedItem = { ...item, ...updates };

    await new Promise((resolve, reject) => {
      const request = store.put(updatedItem);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });

    console.log(`✅ Sync queue item mis à jour: ${id}`);
    return true;
  } catch (error) {
    console.error('❌ Erreur updateSyncQueueItem:', error);
    return false;
  }
}

// Supprimer de la file de synchronisation
export async function removeFromSyncQueue(id) {
  try {
    const db = await openDB();
    const transaction = db.transaction([STORES.SYNC_QUEUE], 'readwrite');
    const store = transaction.objectStore(STORES.SYNC_QUEUE);

    await new Promise((resolve, reject) => {
      const request = store.delete(id);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });

    console.log(`🗑️ Supprimé de la queue: ${id}`);
    return true;
  } catch (error) {
    console.error('❌ Erreur removeFromSyncQueue:', error);
    return false;
  }
}

// Vider la file de synchronisation
export async function clearSyncQueue() {
  try {
    const db = await openDB();
    const transaction = db.transaction([STORES.SYNC_QUEUE], 'readwrite');
    const store = transaction.objectStore(STORES.SYNC_QUEUE);

    await new Promise((resolve, reject) => {
      const request = store.clear();
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });

    console.log('🗑️ Queue de synchronisation vidée');
    return true;
  } catch (error) {
    console.error('❌ Erreur clearSyncQueue:', error);
    return false;
  }
}

/**
 * GENERIC CRUD OPERATIONS
 */

// Créer/Mettre à jour
export async function set(storeName, key, value) {
  try {
    const db = await openDB();
    const transaction = db.transaction([storeName], 'readwrite');
    const store = transaction.objectStore(storeName);

    await new Promise((resolve, reject) => {
      const request = store.put({ id: key, ...value });
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });

    return true;
  } catch (error) {
    console.error(`❌ Erreur set (${storeName}):`, error);
    return false;
  }
}

// Lire
export async function get(storeName, key) {
  try {
    const db = await openDB();
    const transaction = db.transaction([storeName], 'readonly');
    const store = transaction.objectStore(storeName);

    const result = await new Promise((resolve, reject) => {
      const request = store.get(key);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    return result;
  } catch (error) {
    console.error(`❌ Erreur get (${storeName}):`, error);
    return null;
  }
}

// Lire tout
export async function getAll(storeName) {
  try {
    const db = await openDB();
    const transaction = db.transaction([storeName], 'readonly');
    const store = transaction.objectStore(storeName);

    const results = await new Promise((resolve, reject) => {
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });

    return results;
  } catch (error) {
    console.error(`❌ Erreur getAll (${storeName}):`, error);
    return [];
  }
}

// Supprimer
export async function remove(storeName, key) {
  try {
    const db = await openDB();
    const transaction = db.transaction([storeName], 'readwrite');
    const store = transaction.objectStore(storeName);

    await new Promise((resolve, reject) => {
      const request = store.delete(key);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });

    return true;
  } catch (error) {
    console.error(`❌ Erreur remove (${storeName}):`, error);
    return false;
  }
}

// Vider un store
export async function clear(storeName) {
  try {
    const db = await openDB();
    const transaction = db.transaction([storeName], 'readwrite');
    const store = transaction.objectStore(storeName);

    await new Promise((resolve, reject) => {
      const request = store.clear();
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });

    return true;
  } catch (error) {
    console.error(`❌ Erreur clear (${storeName}):`, error);
    return false;
  }
}

/**
 * UTILITIES
 */

// Obtenir la taille de la base de données
export async function getDBSize() {
  try {
    if ('storage' in navigator && 'estimate' in navigator.storage) {
      const estimate = await navigator.storage.estimate();
      return {
        usage: estimate.usage,
        quota: estimate.quota,
        usageInMB: (estimate.usage / (1024 * 1024)).toFixed(2),
        quotaInMB: (estimate.quota / (1024 * 1024)).toFixed(2),
        percentageUsed: ((estimate.usage / estimate.quota) * 100).toFixed(2),
      };
    }
    return null;
  } catch (error) {
    console.error('❌ Erreur getDBSize:', error);
    return null;
  }
}

// Exporter toutes les données
export async function exportData() {
  try {
    const data = {};

    for (const storeName of Object.values(STORES)) {
      data[storeName] = await getAll(storeName);
    }

    return data;
  } catch (error) {
    console.error('❌ Erreur exportData:', error);
    return null;
  }
}

// Supprimer toute la base de données
export async function deleteDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.deleteDatabase(DB_NAME);

    request.onsuccess = () => {
      console.log('🗑️ Base de données supprimée');
      resolve(true);
    };

    request.onerror = () => {
      console.error('❌ Erreur suppression DB:', request.error);
      reject(request.error);
    };

    request.onblocked = () => {
      console.warn('⚠️ Suppression DB bloquée (fermer tous les onglets)');
    };
  });
}

// Export des constantes
export { STORES, CACHE_TTL };

// Export par défaut
export default {
  // Cache
  setCache,
  getCache,
  deleteCache,
  clearCache,
  cleanExpiredCache,

  // Sync Queue
  addToSyncQueue,
  getSyncQueue,
  updateSyncQueueItem,
  removeFromSyncQueue,
  clearSyncQueue,

  // CRUD
  set,
  get,
  getAll,
  remove,
  clear,

  // Utils
  getDBSize,
  exportData,
  deleteDatabase,

  // Constants
  STORES,
  CACHE_TTL,
};
