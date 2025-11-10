/**
 * Advanced Search Page
 * Full-featured search with Elasticsearch
 */
import React, { useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import useAdvancedSearch, { useAutocomplete } from '../hooks/useAdvancedSearch';
import OptimizedImage from '../components/common/OptimizedImage';

// Icons (replace with your icon library)
const SearchIcon = () => <span>🔍</span>;
const FilterIcon = () => <span>🔧</span>;
const CloseIcon = () => <span>✕</span>;
const StarIcon = () => <span>⭐</span>;

const AdvancedSearchPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  // Initialize from URL params
  const initialQuery = searchParams.get('q') || '';
  const initialFilters = {
    category: searchParams.get('category') || null,
    minPrice: searchParams.get('min_price') ? parseFloat(searchParams.get('min_price')) : null,
    maxPrice: searchParams.get('max_price') ? parseFloat(searchParams.get('max_price')) : null,
    minRating: searchParams.get('min_rating') ? parseFloat(searchParams.get('min_rating')) : null
  };

  // Search hook
  const {
    query,
    filters,
    results,
    total,
    facets,
    isLoading,
    error,
    page,
    totalPages,
    sortBy,
    updateQuery,
    updateFilters,
    clearFilters,
    updateSort,
    goToPage,
    trackProductClick,
    hasResults,
    isEmpty
  } = useAdvancedSearch(initialQuery, initialFilters);

  // Local state
  const [inputValue, setInputValue] = useState(initialQuery);
  const [showFilters, setShowFilters] = useState(false);
  const [showAutocomplete, setShowAutocomplete] = useState(false);

  // Autocomplete
  const { suggestions } = useAutocomplete(inputValue);

  // Handlers
  const handleSearchSubmit = (e) => {
    e.preventDefault();
    updateQuery(inputValue);
    setShowAutocomplete(false);
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    setShowAutocomplete(true);
  };

  const handleSuggestionClick = (suggestion) => {
    setInputValue(suggestion);
    updateQuery(suggestion);
    setShowAutocomplete(false);
  };

  const handleProductClick = (product) => {
    trackProductClick(product.id);
    navigate(`/marketplace/product/${product.id}`);
  };

  const handleFilterChange = (filterName, value) => {
    updateFilters({ [filterName]: value });
  };

  const handleClearFilters = () => {
    clearFilters();
    setInputValue('');
  };

  return (
    <div className="advanced-search-page min-h-screen bg-gray-50">
      {/* Search Header */}
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          {/* Search Bar */}
          <form onSubmit={handleSearchSubmit} className="relative">
            <div className="relative">
              <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                onFocus={() => setShowAutocomplete(true)}
                onBlur={() => setTimeout(() => setShowAutocomplete(false), 200)}
                placeholder="Rechercher des produits..."
                className="w-full px-12 py-3 rounded-lg border-2 border-gray-300 focus:border-indigo-500 focus:outline-none text-lg"
              />
              <SearchIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" />

              {inputValue && (
                <button
                  type="button"
                  onClick={() => {
                    setInputValue('');
                    updateQuery('');
                  }}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <CloseIcon />
                </button>
              )}
            </div>

            {/* Autocomplete Dropdown */}
            {showAutocomplete && suggestions.length > 0 && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg z-20">
                {suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="w-full px-4 py-3 text-left hover:bg-gray-100 flex items-center gap-3"
                  >
                    <SearchIcon className="text-gray-400" />
                    <span>{suggestion}</span>
                  </button>
                ))}
              </div>
            )}
          </form>

          {/* Filters Button & Active Filters */}
          <div className="mt-4 flex items-center gap-3 flex-wrap">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center gap-2 px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200"
            >
              <FilterIcon />
              <span>Filtres</span>
            </button>

            {/* Active Filters */}
            {filters.category && (
              <span className="px-3 py-1 bg-gray-200 rounded-full text-sm flex items-center gap-2">
                Catégorie: {filters.category}
                <button onClick={() => handleFilterChange('category', null)}>
                  <CloseIcon />
                </button>
              </span>
            )}

            {filters.minPrice && (
              <span className="px-3 py-1 bg-gray-200 rounded-full text-sm flex items-center gap-2">
                Prix min: {filters.minPrice} MAD
                <button onClick={() => handleFilterChange('minPrice', null)}>
                  <CloseIcon />
                </button>
              </span>
            )}

            {filters.maxPrice && (
              <span className="px-3 py-1 bg-gray-200 rounded-full text-sm flex items-center gap-2">
                Prix max: {filters.maxPrice} MAD
                <button onClick={() => handleFilterChange('maxPrice', null)}>
                  <CloseIcon />
                </button>
              </span>
            )}

            {(filters.category || filters.minPrice || filters.maxPrice) && (
              <button
                onClick={handleClearFilters}
                className="text-sm text-red-600 hover:text-red-700 underline"
              >
                Effacer tout
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex gap-6">
          {/* Sidebar Filters */}
          {showFilters && (
            <div className="w-64 flex-shrink-0">
              <div className="bg-white rounded-lg shadow-sm p-6 sticky top-24">
                <h3 className="font-bold text-lg mb-4">Filtres</h3>

                {/* Category Filter */}
                {facets.categories && facets.categories.length > 0 && (
                  <div className="mb-6">
                    <h4 className="font-semibold mb-2">Catégorie</h4>
                    {facets.categories.map((cat) => (
                      <label key={cat.key} className="flex items-center gap-2 mb-2">
                        <input
                          type="radio"
                          name="category"
                          checked={filters.category === cat.key}
                          onChange={() => handleFilterChange('category', cat.key)}
                        />
                        <span className="text-sm">
                          {cat.key} ({cat.count})
                        </span>
                      </label>
                    ))}
                  </div>
                )}

                {/* Price Range */}
                <div className="mb-6">
                  <h4 className="font-semibold mb-2">Prix (MAD)</h4>
                  <div className="space-y-2">
                    <input
                      type="number"
                      placeholder="Min"
                      value={filters.minPrice || ''}
                      onChange={(e) => handleFilterChange('minPrice', parseFloat(e.target.value) || null)}
                      className="w-full px-3 py-2 border rounded"
                    />
                    <input
                      type="number"
                      placeholder="Max"
                      value={filters.maxPrice || ''}
                      onChange={(e) => handleFilterChange('maxPrice', parseFloat(e.target.value) || null)}
                      className="w-full px-3 py-2 border rounded"
                    />
                  </div>
                </div>

                {/* Rating Filter */}
                <div className="mb-6">
                  <h4 className="font-semibold mb-2">Note minimum</h4>
                  {[4, 3, 2, 1].map((rating) => (
                    <label key={rating} className="flex items-center gap-2 mb-2">
                      <input
                        type="radio"
                        name="rating"
                        checked={filters.minRating === rating}
                        onChange={() => handleFilterChange('minRating', rating)}
                      />
                      <span className="text-sm flex items-center">
                        {rating} <StarIcon /> et plus
                      </span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Results */}
          <div className="flex-1">
            {/* Results Header */}
            <div className="bg-white rounded-lg shadow-sm p-4 mb-4 flex items-center justify-between">
              <div className="text-gray-600">
                {isLoading ? (
                  'Recherche en cours...'
                ) : (
                  `${total} résultat${total > 1 ? 's' : ''}`
                )}
              </div>

              {/* Sort */}
              <select
                value={sortBy}
                onChange={(e) => updateSort(e.target.value)}
                className="px-4 py-2 border rounded-lg"
              >
                <option value="relevance">Pertinence</option>
                <option value="newest">Plus récents</option>
                <option value="price_asc">Prix croissant</option>
                <option value="price_desc">Prix décroissant</option>
                <option value="rating">Meilleures notes</option>
                <option value="popular">Plus populaires</option>
              </select>
            </div>

            {/* Loading */}
            {isLoading && (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-indigo-500 border-t-transparent"></div>
                <p className="mt-4 text-gray-600">Recherche en cours...</p>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
                {error}
              </div>
            )}

            {/* Empty State */}
            {isEmpty && !isLoading && (
              <div className="text-center py-12">
                <SearchIcon className="text-6xl text-gray-300 mb-4" />
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  Aucun résultat trouvé
                </h3>
                <p className="text-gray-500 mb-4">
                  Essayez d'autres mots-clés ou modifiez vos filtres
                </p>
                <button
                  onClick={handleClearFilters}
                  className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                >
                  Effacer les filtres
                </button>
              </div>
            )}

            {/* Results Grid */}
            {hasResults && !isLoading && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {results.map((product) => (
                    <div
                      key={product.id}
                      onClick={() => handleProductClick(product)}
                      className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer overflow-hidden"
                    >
                      <OptimizedImage
                        src={product.image_url}
                        alt={product.name}
                        width={400}
                        height={300}
                        className="w-full h-48 object-cover"
                      />

                      <div className="p-4">
                        <h3 className="font-semibold text-lg mb-2 line-clamp-2">
                          {product.name}
                        </h3>

                        <p className="text-gray-600 text-sm mb-2 line-clamp-2">
                          {product.description}
                        </p>

                        <div className="flex items-center justify-between mt-4">
                          <div>
                            <span className="text-2xl font-bold text-indigo-600">
                              {product.price} MAD
                            </span>
                            {product.original_price > product.price && (
                              <span className="text-sm text-gray-400 line-through ml-2">
                                {product.original_price} MAD
                              </span>
                            )}
                          </div>

                          {product.rating > 0 && (
                            <div className="flex items-center gap-1">
                              <StarIcon className="text-yellow-400" />
                              <span className="font-semibold">{product.rating.toFixed(1)}</span>
                            </div>
                          )}
                        </div>

                        <div className="mt-3 text-sm text-gray-500">
                          {product.merchant_name}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="mt-8 flex justify-center items-center gap-2">
                    <button
                      onClick={() => goToPage(page - 1)}
                      disabled={page === 1}
                      className="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                    >
                      Précédent
                    </button>

                    {[...Array(totalPages)].map((_, i) => {
                      const pageNum = i + 1;

                      // Show first 3, last 3, and current +/- 2
                      if (
                        pageNum <= 3 ||
                        pageNum > totalPages - 3 ||
                        (pageNum >= page - 2 && pageNum <= page + 2)
                      ) {
                        return (
                          <button
                            key={pageNum}
                            onClick={() => goToPage(pageNum)}
                            className={`px-4 py-2 border rounded-lg ${
                              page === pageNum
                                ? 'bg-indigo-600 text-white'
                                : 'hover:bg-gray-50'
                            }`}
                          >
                            {pageNum}
                          </button>
                        );
                      } else if (pageNum === 4 || pageNum === totalPages - 3) {
                        return <span key={pageNum}>...</span>;
                      }

                      return null;
                    })}

                    <button
                      onClick={() => goToPage(page + 1)}
                      disabled={page === totalPages}
                      className="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                    >
                      Suivant
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdvancedSearchPage;
