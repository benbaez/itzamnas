#!/usr/bin/env python3

import os
from elasticsearch import Elasticsearch
from datetime import datetime

import common_func
import elastic_func

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = script_directory + '/config.yaml'
variables = common_func.load_variables_from_yaml(file_path)

    
elastic_func.es_conn_check()
    
# Define index name
es_index_name = "conversations_stream"

# Create index if it doesn't exist
elastic_func.es_index_create(es_index_name)


def process_conversation_results(results):
    # Extract relevant data
    hits = results['hits']['hits']

    # Process and convert data
    for hit in hits:
        source_data = hit['_source']
    
        # Example: Accessing individual fields and assigning them to variables
        variable1 = source_data['user_input']
        variable2 = source_data['bot_response']
    
        # Example: Printing the variables
        print(f"Variable 1: {variable1}, Variable 2: {variable2}")

# Example usage
elastic_func.es_store_conv(es_index_name, "Hello, how are you?", "I am doing well, thank you for asking.")
elastic_func.es_store_conv(es_index_name, "What is the weather like today?", "The weather is sunny with a high of 25 degrees Celsius.")
    
print("Conversations stored successfully.")

# Define the index and query
query = {
    "query": {
        "match_all": {} # Or any other query
    }
}

# Retrieve data
try:
    results = elastic_func.es_search_for_conv(es_index_name, query)

    # Process and print results
    for hit in results['hits']['hits']:
        print(hit['_source'])

    # Process into variables
    process_conversation_results(results)

except Exception as e:
    print(f"Error retrieving data: {e}")
