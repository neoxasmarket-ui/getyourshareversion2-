"""
Advanced Search Service with Elasticsearch
- Full-text search with fuzzy matching
- Autocomplete suggestions
- Faceted search (filters)
- Search analytics & tracking
- Real-time indexing
"""
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import NotFoundError, RequestError

from utils.logger import logger
from services.advanced_caching import cache_service


class ElasticsearchService:
    """Advanced search powered by Elasticsearch"""

    def __init__(self):
        # Connect to Elasticsearch
        self.es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
        self.es_port = int(os.getenv('ELASTICSEARCH_PORT', 9200))
        self.es_user = os.getenv('ELASTICSEARCH_USER', 'elastic')
        self.es_password = os.getenv('ELASTICSEARCH_PASSWORD', '')

        try:
            self.es = Elasticsearch(
                [f'http://{self.es_host}:{self.es_port}'],
                basic_auth=(self.es_user, self.es_password) if self.es_password else None,
                verify_certs=False,
                request_timeout=30
            )

            if self.es.ping():
                logger.info(f"✅ Elasticsearch connected: {self.es_host}:{self.es_port}")
                self.available = True
            else:
                logger.warning("❌ Elasticsearch not available")
                self.available = False

        except Exception as e:
            logger.error(f"Elasticsearch connection failed: {e}")
            self.available = False

        # Index names
        self.indexes = {
            'products': 'getyourshare_products',
            'users': 'getyourshare_users',
            'merchants': 'getyourshare_merchants',
            'influencers': 'getyourshare_influencers'
        }

    # ========================================
    # INDEX MANAGEMENT
    # ========================================

    async def create_indexes(self):
        """Create all search indexes with mappings"""
        if not self.available:
            logger.warning("Elasticsearch not available, skipping index creation")
            return

        # Products index
        await self._create_products_index()

        # Users index
        await self._create_users_index()

        # Merchants index
        await self._create_merchants_index()

        # Influencers index
        await self._create_influencers_index()

        logger.info("✅ All Elasticsearch indexes created")

    async def _create_products_index(self):
        """Create products index with custom mapping"""
        index_name = self.indexes['products']

        if self.es.indices.exists(index=index_name):
            logger.info(f"Index {index_name} already exists")
            return

        mapping = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1,
                "analysis": {
                    "analyzer": {
                        "autocomplete_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["lowercase", "autocomplete_filter"]
                        },
                        "search_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["lowercase"]
                        }
                    },
                    "filter": {
                        "autocomplete_filter": {
                            "type": "edge_ngram",
                            "min_gram": 2,
                            "max_gram": 20
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {
                        "type": "text",
                        "analyzer": "autocomplete_analyzer",
                        "search_analyzer": "search_analyzer",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "suggest": {
                                "type": "completion"
                            }
                        }
                    },
                    "description": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "category": {
                        "type": "keyword"
                    },
                    "sub_category": {
                        "type": "keyword"
                    },
                    "price": {"type": "float"},
                    "original_price": {"type": "float"},
                    "discount_percentage": {"type": "integer"},
                    "merchant_id": {"type": "keyword"},
                    "merchant_name": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword"}}
                    },
                    "rating": {"type": "float"},
                    "reviews_count": {"type": "integer"},
                    "sales_count": {"type": "integer"},
                    "status": {"type": "keyword"},
                    "tags": {"type": "keyword"},
                    "image_url": {"type": "keyword"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"},
                    "location": {"type": "geo_point"},
                    "metadata": {"type": "object", "enabled": False}
                }
            }
        }

        self.es.indices.create(index=index_name, body=mapping)
        logger.info(f"✅ Created index: {index_name}")

    async def _create_users_index(self):
        """Create users index"""
        index_name = self.indexes['users']

        if self.es.indices.exists(index=index_name):
            return

        mapping = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "suggest": {"type": "completion"}
                        }
                    },
                    "email": {"type": "keyword"},
                    "role": {"type": "keyword"},
                    "created_at": {"type": "date"}
                }
            }
        }

        self.es.indices.create(index=index_name, body=mapping)
        logger.info(f"✅ Created index: {index_name}")

    async def _create_merchants_index(self):
        """Create merchants index"""
        index_name = self.indexes['merchants']

        if self.es.indices.exists(index=index_name):
            return

        mapping = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {
                        "type": "text",
                        "analyzer": "autocomplete_analyzer",
                        "search_analyzer": "search_analyzer",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "suggest": {"type": "completion"}
                        }
                    },
                    "category": {"type": "keyword"},
                    "rating": {"type": "float"},
                    "products_count": {"type": "integer"},
                    "location": {"type": "geo_point"}
                }
            }
        }

        self.es.indices.create(index=index_name, body=mapping)
        logger.info(f"✅ Created index: {index_name}")

    async def _create_influencers_index(self):
        """Create influencers index"""
        index_name = self.indexes['influencers']

        if self.es.indices.exists(index=index_name):
            return

        mapping = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "suggest": {"type": "completion"}
                        }
                    },
                    "niche": {"type": "keyword"},
                    "followers": {"type": "integer"},
                    "engagement_rate": {"type": "float"}
                }
            }
        }

        self.es.indices.create(index=index_name, body=mapping)
        logger.info(f"✅ Created index: {index_name}")

    # ========================================
    # INDEXING (ADD/UPDATE/DELETE)
    # ========================================

    async def index_product(self, product: Dict[str, Any]):
        """Index a single product"""
        if not self.available:
            return

        index_name = self.indexes['products']

        # Prepare document
        doc = {
            'id': str(product['id']),
            'name': product['name'],
            'description': product.get('description', ''),
            'category': product.get('category', 'uncategorized'),
            'sub_category': product.get('sub_category'),
            'price': float(product.get('price', 0)),
            'original_price': float(product.get('original_price', 0)),
            'discount_percentage': int(product.get('discount_percentage', 0)),
            'merchant_id': str(product.get('merchant_id')),
            'merchant_name': product.get('merchant_name', ''),
            'rating': float(product.get('rating', 0)),
            'reviews_count': int(product.get('reviews_count', 0)),
            'sales_count': int(product.get('sales_count', 0)),
            'status': product.get('status', 'active'),
            'tags': product.get('tags', []),
            'image_url': product.get('image_url', ''),
            'created_at': product.get('created_at'),
            'updated_at': datetime.utcnow().isoformat(),
            'metadata': product.get('metadata', {})
        }

        # Add location if available
        if 'latitude' in product and 'longitude' in product:
            doc['location'] = {
                'lat': product['latitude'],
                'lon': product['longitude']
            }

        # Index document
        self.es.index(
            index=index_name,
            id=str(product['id']),
            document=doc
        )

        logger.debug(f"Indexed product: {product['name']}")

    async def bulk_index_products(self, products: List[Dict[str, Any]]):
        """Bulk index multiple products (faster)"""
        if not self.available or not products:
            return

        index_name = self.indexes['products']

        # Prepare bulk actions
        actions = []
        for product in products:
            doc = {
                '_index': index_name,
                '_id': str(product['id']),
                '_source': {
                    'id': str(product['id']),
                    'name': product['name'],
                    'description': product.get('description', ''),
                    'category': product.get('category', 'uncategorized'),
                    'price': float(product.get('price', 0)),
                    'merchant_name': product.get('merchant_name', ''),
                    'rating': float(product.get('rating', 0)),
                    'status': product.get('status', 'active'),
                    'updated_at': datetime.utcnow().isoformat()
                }
            }
            actions.append(doc)

        # Bulk insert
        success, failed = helpers.bulk(self.es, actions, raise_on_error=False)

        logger.info(f"✅ Bulk indexed {success} products, {len(failed)} failed")

    async def delete_product(self, product_id: str):
        """Delete a product from index"""
        if not self.available:
            return

        index_name = self.indexes['products']

        try:
            self.es.delete(index=index_name, id=product_id)
            logger.debug(f"Deleted product: {product_id}")
        except NotFoundError:
            logger.warning(f"Product not found in index: {product_id}")

    # ========================================
    # SEARCH
    # ========================================

    async def search_products(
        self,
        query: str = "",
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        merchant_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = "relevance",  # relevance, price_asc, price_desc, rating, newest
        page: int = 1,
        page_size: int = 20,
        location: Optional[Dict[str, float]] = None,  # {"lat": 33.5, "lon": -7.6}
        radius_km: float = 50.0
    ) -> Dict[str, Any]:
        """
        Advanced product search with filters

        Returns:
            {
                'results': [...],
                'total': 1234,
                'page': 1,
                'page_size': 20,
                'facets': {...},
                'suggestions': [...]
            }
        """
        if not self.available:
            return {'results': [], 'total': 0, 'page': 1, 'page_size': page_size}

        # Build query
        must_queries = []
        filter_queries = [{"term": {"status": "active"}}]

        # Full-text search
        if query:
            must_queries.append({
                "multi_match": {
                    "query": query,
                    "fields": ["name^3", "description^2", "merchant_name", "tags"],
                    "fuzziness": "AUTO",
                    "operator": "or"
                }
            })

        # Category filter
        if category:
            filter_queries.append({"term": {"category": category}})

        # Price range
        if min_price is not None or max_price is not None:
            price_range = {}
            if min_price is not None:
                price_range['gte'] = min_price
            if max_price is not None:
                price_range['lte'] = max_price
            filter_queries.append({"range": {"price": price_range}})

        # Rating filter
        if min_rating is not None:
            filter_queries.append({"range": {"rating": {"gte": min_rating}}})

        # Merchant filter
        if merchant_id:
            filter_queries.append({"term": {"merchant_id": merchant_id}})

        # Tags filter
        if tags:
            filter_queries.append({"terms": {"tags": tags}})

        # Location filter (geo_distance)
        if location:
            filter_queries.append({
                "geo_distance": {
                    "distance": f"{radius_km}km",
                    "location": {
                        "lat": location['lat'],
                        "lon": location['lon']
                    }
                }
            })

        # Build final query
        es_query = {
            "bool": {
                "must": must_queries if must_queries else [{"match_all": {}}],
                "filter": filter_queries
            }
        }

        # Sorting
        sort_options = {
            "relevance": [{"_score": "desc"}],
            "price_asc": [{"price": "asc"}],
            "price_desc": [{"price": "desc"}],
            "rating": [{"rating": "desc"}],
            "newest": [{"created_at": "desc"}],
            "popular": [{"sales_count": "desc"}]
        }
        sort = sort_options.get(sort_by, sort_options['relevance'])

        # Pagination
        from_param = (page - 1) * page_size

        # Aggregations (facets)
        aggs = {
            "categories": {
                "terms": {"field": "category", "size": 20}
            },
            "price_ranges": {
                "histogram": {
                    "field": "price",
                    "interval": 100
                }
            },
            "avg_rating": {
                "avg": {"field": "rating"}
            },
            "price_stats": {
                "stats": {"field": "price"}
            }
        }

        # Execute search
        try:
            response = self.es.search(
                index=self.indexes['products'],
                query=es_query,
                sort=sort,
                from_=from_param,
                size=page_size,
                aggs=aggs,
                track_total_hits=True
            )

            # Extract results
            hits = response['hits']['hits']
            results = [hit['_source'] for hit in hits]
            total = response['hits']['total']['value']

            # Extract facets
            facets = {
                'categories': [
                    {'key': bucket['key'], 'count': bucket['doc_count']}
                    for bucket in response['aggregations']['categories']['buckets']
                ],
                'price_ranges': [
                    {'min': bucket['key'], 'max': bucket['key'] + 100, 'count': bucket['doc_count']}
                    for bucket in response['aggregations']['price_ranges']['buckets']
                ],
                'avg_rating': response['aggregations']['avg_rating']['value'],
                'price_stats': response['aggregations']['price_stats']
            }

            # Get suggestions if query exists
            suggestions = []
            if query:
                suggestions = await self.get_suggestions(query, limit=5)

            result = {
                'results': results,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size,
                'facets': facets,
                'suggestions': suggestions,
                'query': query,
                'filters': {
                    'category': category,
                    'price_range': {'min': min_price, 'max': max_price},
                    'min_rating': min_rating
                }
            }

            # Cache results for 5 minutes
            cache_key = f"search:{hash(str(es_query))}"
            cache_service.set(cache_key, result, ttl=300)

            return result

        except RequestError as e:
            logger.error(f"Elasticsearch search error: {e}")
            return {'results': [], 'total': 0, 'page': 1, 'page_size': page_size}

    # ========================================
    # AUTOCOMPLETE & SUGGESTIONS
    # ========================================

    async def get_suggestions(self, query: str, limit: int = 10) -> List[str]:
        """Get autocomplete suggestions"""
        if not self.available or not query:
            return []

        try:
            response = self.es.search(
                index=self.indexes['products'],
                suggest={
                    "product_suggest": {
                        "prefix": query,
                        "completion": {
                            "field": "name.suggest",
                            "size": limit,
                            "skip_duplicates": True
                        }
                    }
                }
            )

            suggestions = [
                option['text']
                for option in response['suggest']['product_suggest'][0]['options']
            ]

            return suggestions

        except Exception as e:
            logger.error(f"Suggestion error: {e}")
            return []

    async def get_popular_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular search queries"""
        # This would query a search_analytics index
        # For now, return mock data
        return [
            {'query': 'iphone 15', 'count': 1250},
            {'query': 'nike shoes', 'count': 980},
            {'query': 'laptop gaming', 'count': 750}
        ]

    # ========================================
    # ANALYTICS
    # ========================================

    async def track_search(
        self,
        query: str,
        user_id: Optional[str] = None,
        results_count: int = 0,
        clicked_product: Optional[str] = None
    ):
        """Track search for analytics"""
        # Index to search_analytics index
        analytics_index = 'getyourshare_search_analytics'

        doc = {
            'query': query,
            'user_id': user_id,
            'results_count': results_count,
            'clicked_product': clicked_product,
            'timestamp': datetime.utcnow().isoformat()
        }

        try:
            self.es.index(index=analytics_index, document=doc)
        except Exception as e:
            logger.error(f"Search tracking error: {e}")


# Global instance
search_service = ElasticsearchService()


# Initialize indexes on startup
async def init_search_indexes():
    """Call this on app startup"""
    await search_service.create_indexes()


# Example FastAPI endpoints
if __name__ == "__main__":
    """
    from fastapi import APIRouter, Query

    router = APIRouter(prefix="/api/search")

    @router.get("/products")
    async def search_products(
        q: str = Query("", description="Search query"),
        category: str = None,
        min_price: float = None,
        max_price: float = None,
        min_rating: float = None,
        sort_by: str = "relevance",
        page: int = 1,
        page_size: int = 20
    ):
        results = await search_service.search_products(
            query=q,
            category=category,
            min_price=min_price,
            max_price=max_price,
            min_rating=min_rating,
            sort_by=sort_by,
            page=page,
            page_size=page_size
        )
        return results

    @router.get("/suggestions")
    async def get_suggestions(q: str = Query(..., min_length=2)):
        suggestions = await search_service.get_suggestions(q, limit=10)
        return {'suggestions': suggestions}
    """
    pass
