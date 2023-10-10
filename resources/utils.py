# srcs/searchengine/utils.py
# We define that each airbnb has five properties 
def check_and_create_index(es, index: str):
    # Define data model
    mappings = {
        'mappings': {
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type': 'text'},
                'host_id': {'type': 'integer'},
                'host_name': {'type': 'keyword'},
                'neighbourhood_group': {'type': 'keyword'},
                'neighbourhood': {'type': 'keyword'},
                'latitude': {'type': 'float'},
                'longitude': {'type': 'float'},
                'room_type': {'type': 'keyword'},
                'price': {'type': 'integer'},
                'minimum_nights': {'type': 'integer'},
                'number_of_reviews': {'type': 'integer'},
                'last_review': {'type': 'date', 'format': 'yyyy-MM-dd'},
                'reviews_per_month': {'type': 'float'},
                'calculated_host_listings_count': {'type': 'integer'},
                'availability_365': {'type': 'integer'}
            }
        }
    }
    
    if not es.indices.exists(index):
        es.indices.create(index=index, body=mappings, ignore=400)

def index_search(es, index: str, keywords: str, filters: str, from_i: int, size: int, price_range: int) -> dict:
    """
    Args:
        es: Elasticsearch client instance.
        index: Name of the index we are going to use.
        keywords: Search keywords.
        filters: Field name to filter airbnbs.
        from_i: Start index of the results for pagination.
        size: Number of results returned in each search.
    """
    body = {
        'query': {
            'bool': {
                'must': [],
                'filter': []
            }
        },
        'highlight': {
            'pre_tags': ['<b>'],
            'post_tags': ['</b>'],
            'fields': {'name': {}, 'host_name': {}, 'neighbourhood': {}}
        },
        'from': from_i,
        'size': size,
        'aggs': {
            'neighbourhood_group': {
                'terms': {'field': 'neighbourhood_group.keyword'}
            },
            'room_type': {
                'terms': {'field': 'room_type.keyword'}
            }
        }
    }
    
    if keywords:
        body['query']['bool']['must'].append({
            'multi_match': {
                'query': keywords,
                'fields': ['name', 'host_name', 'neighbourhood']
            }
        })
    
    if filters:
        body['query']['bool']['filter'] = {
            'term': {
                filters: True
            }
        }

    if price_range:
        body['query']['bool']['filter'].append({
            'range': {
                'price': {
                    'gte': price_range[0],
                    'lte': price_range[1]
                }
            }
        })
    
    
    res = es.search(index=index, body=body)
    
    sorted_neighbourhood_groups = res['aggregations']['neighbourhood_group']['buckets']
    sorted_neighbourhood_groups = sorted(
        sorted_neighbourhood_groups,
        key=lambda t: t['doc_count'], reverse=True
    )
    res['sorted_neighbourhood_groups'] = [t['key'] for t in sorted_neighbourhood_groups]
    
    sorted_room_types = res['aggregations']['room_type']['buckets']
    sorted_room_types = sorted(
        sorted_room_types,
        key=lambda t: t['doc_count'], reverse=True
    )
    res['sorted_room_types'] = [t['key'] for t in sorted_room_types]
    
    return res



def calculate_average_price_by_neighborhood(es, index):
    """
    Calculates the average price per neighborhood.

    Args:
        es: Elasticsearch client instance.
        index: Name of the index.

    Returns:
        A dictionary containing neighborhood names as keys and average prices as values.
    """
    # Define the Elasticsearch query body
    body = {
        'size': 0,  # We don't need search results, only aggregations
        'aggs': {
            'neighborhoods': {
                'terms': {
                    'field': 'neighbourhood.keyword',  # Aggregate by neighborhood field
                    'size': 1000  # Adjust the size based on the number of neighborhoods in your data
                },
                'aggs': {
                    'avg_price': {
                        'avg': {
                            'field': 'price'  # Calculate the average price for each neighborhood
                        }
                    }
                }
            }
        }
    }

    # Execute the Elasticsearch search
    res = es.search(index=index, body=body)

    avg_prices_by_neighborhood = {}
    for bucket in res['aggregations']['neighborhoods']['buckets']:
        neighborhood = bucket['key']  # Get the neighborhood name
        avg_price = bucket['avg_price']['value']  # Get the average price
        avg_prices_by_neighborhood[neighborhood] = avg_price

    return avg_prices_by_neighborhood