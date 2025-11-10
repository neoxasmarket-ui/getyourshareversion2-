/**
 * Advanced Search Hook with Elasticsearch
 * Features:
 * - Full-text search with fuzzy matching
 * - Debounced search
 * - Faceted filters
 * - Autocomplete
 * - Search analytics tracking
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';

const useAdvancedSearch = (initialQuery = '', initialFilters = {}) => {
  // State
  const [query, setQuery] = useState(initialQuery);
  const [filters, setFilters] = useState({
    category: initialFilters.category || null,
    minPrice: initialFilters.minPrice || null,
    maxPrice: initialFilters.maxPrice || null,
    minRating: initialFilters.minRating || null,
    tags: initialFilters.tags || [],
    ...initialFilters
  });

  const [results, setResults] = useState([]);
  const [total, setTotal] = useState(0);
  const [facets, setFacets] = useState({});
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [sortBy, setSortBy] = useState('relevance');

  // Refs
  const debounceTimer = useRef(null);
  const abortController = useRef(null);

  /**
   * Perform search with current query and filters
   */
  const performSearch = useCallback(async () => {
    // Cancel previous request
    if (abortController.current) {
      abortController.current.abort();
    }

    abortController.current = new AbortController();

    setIsLoading(true);
    setError(null);

    try {
      // Build query params
      const params = new URLSearchParams();

      if (query) params.append('q', query);
      if (filters.category) params.append('category', filters.category);
      if (filters.minPrice) params.append('min_price', filters.minPrice);
      if (filters.maxPrice) params.append('max_price', filters.maxPrice);
      if (filters.minRating) params.append('min_rating', filters.minRating);
      if (filters.merchantId) params.append('merchant_id', filters.merchantId);
      if (filters.tags && filters.tags.length > 0) {
        filters.tags.forEach(tag => params.append('tags', tag));
      }

      params.append('sort_by', sortBy);
      params.append('page', page);
      params.append('page_size', pageSize);

      // Execute search
      const response = await axios.get(`/api/search/products?${params.toString()}`, {
        signal: abortController.current.signal
      });

      const data = response.data;

      setResults(data.results || []);
      setTotal(data.total || 0);
      setFacets(data.facets || {});
      setSuggestions(data.suggestions || []);

      // Track search
      trackSearch(query, data.total, null);

    } catch (err) {
      if (err.name !== 'CanceledError') {
        console.error('Search error:', err);
        setError('An error occurred while searching. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [query, filters, sortBy, page, pageSize]);

  /**
   * Debounced search (wait for user to stop typing)
   */
  const debouncedSearch = useCallback(() => {
    // Clear existing timer
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    // Set new timer
    debounceTimer.current = setTimeout(() => {
      performSearch();
    }, 300); // 300ms delay
  }, [performSearch]);

  /**
   * Search with immediate execution (no debounce)
   */
  const search = useCallback(() => {
    performSearch();
  }, [performSearch]);

  /**
   * Update query and trigger debounced search
   */
  const updateQuery = useCallback((newQuery) => {
    setQuery(newQuery);
    setPage(1); // Reset to first page
  }, []);

  /**
   * Update filters and trigger search
   */
  const updateFilters = useCallback((newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
    setPage(1); // Reset to first page
  }, []);

  /**
   * Clear all filters
   */
  const clearFilters = useCallback(() => {
    setFilters({
      category: null,
      minPrice: null,
      maxPrice: null,
      minRating: null,
      tags: []
    });
    setPage(1);
  }, []);

  /**
   * Update sorting
   */
  const updateSort = useCallback((newSortBy) => {
    setSortBy(newSortBy);
    setPage(1);
  }, []);

  /**
   * Go to specific page
   */
  const goToPage = useCallback((newPage) => {
    setPage(newPage);
  }, []);

  /**
   * Track search for analytics
   */
  const trackSearch = useCallback(async (searchQuery, resultsCount, clickedProduct) => {
    try {
      await axios.post('/api/search/track', {
        query: searchQuery,
        results_count: resultsCount,
        clicked_product: clickedProduct
      });
    } catch (err) {
      console.error('Search tracking failed:', err);
    }
  }, []);

  /**
   * Track product click
   */
  const trackProductClick = useCallback((productId) => {
    trackSearch(query, total, productId);
  }, [query, total, trackSearch]);

  // Effect: Perform search when query or filters change (debounced)
  useEffect(() => {
    if (query || Object.values(filters).some(v => v)) {
      debouncedSearch();
    } else {
      // Empty query - show all products
      performSearch();
    }

    // Cleanup
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, [query, debouncedSearch, performSearch]);

  // Effect: Perform search when sort or page changes (immediate)
  useEffect(() => {
    if (page > 1 || sortBy !== 'relevance') {
      search();
    }
  }, [sortBy, page, search]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (abortController.current) {
        abortController.current.abort();
      }
    };
  }, []);

  return {
    // State
    query,
    filters,
    results,
    total,
    facets,
    suggestions,
    isLoading,
    error,
    page,
    pageSize,
    sortBy,

    // Actions
    updateQuery,
    updateFilters,
    clearFilters,
    updateSort,
    goToPage,
    search,
    trackProductClick,

    // Computed
    totalPages: Math.ceil(total / pageSize),
    hasResults: results.length > 0,
    isEmpty: !isLoading && results.length === 0,
    isFirstPage: page === 1,
    isLastPage: page >= Math.ceil(total / pageSize)
  };
};

export default useAdvancedSearch;

/**
 * Hook for autocomplete suggestions
 */
export const useAutocomplete = (query, delay = 200) => {
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const debounceTimer = useRef(null);
  const abortController = useRef(null);

  useEffect(() => {
    // Clear timer
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    // Empty query
    if (!query || query.length < 2) {
      setSuggestions([]);
      return;
    }

    // Debounce suggestions
    debounceTimer.current = setTimeout(async () => {
      // Cancel previous request
      if (abortController.current) {
        abortController.current.abort();
      }

      abortController.current = new AbortController();
      setIsLoading(true);

      try {
        const response = await axios.get(`/api/search/suggestions?q=${encodeURIComponent(query)}`, {
          signal: abortController.current.signal
        });

        setSuggestions(response.data.suggestions || []);
      } catch (err) {
        if (err.name !== 'CanceledError') {
          console.error('Autocomplete error:', err);
        }
      } finally {
        setIsLoading(false);
      }
    }, delay);

    // Cleanup
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
      if (abortController.current) {
        abortController.current.abort();
      }
    };
  }, [query, delay]);

  return { suggestions, isLoading };
};

/**
 * Hook for popular searches
 */
export const usePopularSearches = () => {
  const [popularSearches, setPopularSearches] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPopularSearches = async () => {
      try {
        const response = await axios.get('/api/search/popular');
        setPopularSearches(response.data.searches || []);
      } catch (err) {
        console.error('Failed to fetch popular searches:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPopularSearches();
  }, []);

  return { popularSearches, isLoading };
};
