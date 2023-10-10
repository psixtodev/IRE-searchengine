import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Load the CSV file with pandas
data_url = "https://raw.githubusercontent.com/fenago/datasets/main/AirBnB_NYC_2019.csv"
data_frame = pd.read_csv(data_url)
print("Data loaded into pandas data frame")

# Set up an ElasticSearch client
es_client = Elasticsearch(["http://elastic:elastic@localhost:9200"])

# Create a function to generate Elasticsearch documents (from dataframe)
def create_document(row):
    return {
        "_index": "airbnb",
        "_id": row["id"],
        "_source": {
            "name": row["name"],
            "host_id": row["host_id"],
            "host_name": row["host_name"],
            "neighbourhood_group": row["neighbourhood_group"],
            "neighbourhood": row["neighbourhood"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "room_type": row["room_type"],
            "price": row["price"],
            "minimum_nights": row["minimum_nights"],
            "number_of_reviews": row["number_of_reviews"],
            "last_review": row["last_review"],
            "reviews_per_month": row["reviews_per_month"],
            "calculated_host_listings_count": row["calculated_host_listings_count"],
            "availability_365": row["availability_365"],
        },
    }

# Load the data into Elasticsearch
documents = [create_document(row) for index, row in data_frame.iterrows()]
bulk(es_client, documents) #efficiently load the data
print("Data loaded into Elasticsearch")