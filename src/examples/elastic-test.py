#!/usr/bin/env python3

import os
from elasticsearch import Elasticsearch
from datetime import datetime

import common_func
import elastic_func

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = script_directory + '/config.yaml'
variables = common_func.load_variables_from_yaml(file_path)
store_examples = True

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
if store_examples:
    try:
        timestamp = datetime.now()
        conversation_data = {
            'timestamp': timestamp,
            'user_input': "Hello, how are you?",
            'bot_response_current': "I am doing well, thank you for asking."
        }
        elastic_func.es_store_conv(es_index_name, conversation_data)
        print("Conversations stored successfully.")
    except Exception as e:
        print(f"Error indexing document: {e}")

    try:
        timestamp = datetime.now()
        conversation_data = {
            'timestamp': timestamp,
            'user_input': "What is the weather like today?",
            'bot_response_current': "The weather is sunny with a high of 25 degrees Celsius."
        }
        elastic_func.es_store_conv(es_index_name, conversation_data)
        print("Conversations stored successfully.")
    except Exception as e:
            print(f"Error indexing document: {e}")

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
