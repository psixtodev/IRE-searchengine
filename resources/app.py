# srcs/searchengine/app.py
import streamlit as st
from elasticsearch import Elasticsearch
from utils import *
from templates import *


INDEX = 'airbnb'
PAGE_SIZE = 30  # Number of results to show per page
PAG_SIZE_NEIGHBORHOODS = 5

# Connect to Elasticsearch
es = Elasticsearch(["http://elastic:elastic@localhost:9200"])
check_and_create_index(es, INDEX)


def set_session_state():
    # Set default values
    st.session_state.setdefault('search', None)

    # Get parameters in URL
    para = st.experimental_get_query_params()
    if 'search' in para:
        st.experimental_set_query_params()
        # Decode URL
        new_search = urllib.parse.unquote(para['search'][0])
        st.session_state.search = new_search


def main():
    set_session_state()
    st.write(load_css(), unsafe_allow_html=True)

    # Title and description
    st.title("Elasticsearch Airbnb Search")
    st.write("Search Engine based on Elasticsearch")

    # Search input
    if st.session_state.search is None:
        search = st.text_input('Enter search words:')
    else:
        search = st.text_input('Enter search words:', st.session_state.search)

    # Price range input
    price_min = st.number_input('Minimum Price', value=0)
    price_max = st.number_input('Maximum Price', value=1000)

    # Calculate average price per neighborhood
    avg_prices_by_neighborhood = calculate_average_price_by_neighborhood(es, INDEX)

    # Pagination for displaying neighborhoods
    neighborhoods = list(avg_prices_by_neighborhood.keys())
    num_neighborhoods = len(neighborhoods)
    num_pages = num_neighborhoods // PAG_SIZE_NEIGHBORHOODS + 1

    current_page = st.slider('Page', 1, num_pages, 1)

    start_idx = (current_page - 1) * PAG_SIZE_NEIGHBORHOODS
    end_idx = min(current_page * PAG_SIZE_NEIGHBORHOODS, num_neighborhoods)
    neighborhoods_to_display = neighborhoods[start_idx:end_idx]

    # Display average price by neighborhood
    st.write("Average Price by Neighborhood:")
    for neighborhood in neighborhoods_to_display:
        avg_price = avg_prices_by_neighborhood[neighborhood]
        checkbox_value = st.checkbox(neighborhood)
        if checkbox_value:
            st.write(f"Neighborhood: {neighborhood}, Average Price: ${avg_price:.2f}")

    # Apply filters
    if st.button('Search'):
        price_range = (price_min, price_max)
        # Add room type filter if selected

        results = index_search(es, INDEX, search, '', 0, PAGE_SIZE, price_range)
        total_hits = results['hits']['total']['value']

        # Display search results
        st.write(number_of_results(total_hits, results['took'] / 1000), unsafe_allow_html=True)

        for i, hit in enumerate(results['hits']['hits']):
            source = hit['_source']
            source['url'] = hit['_id']
            
            st.write(search_result(i, hit['_id'], source['name'], source['host_name'],
                                   source['neighbourhood_group'], source['neighbourhood']),
                     unsafe_allow_html=True)


if __name__ == '__main__':
    main()
