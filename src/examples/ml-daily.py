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
es_index_name = "conversation_qa"

def process_conversation_results(results):
    # Extract relevant data
    hits = results['hits']['hits']

    # Process and convert data
    for hit in hits:
        source_data = hit['_source']

        # print( source_data  )
    
        # Example: Accessing individual fields and assigning them to variables
        variable1 = source_data['bot_current']
        variable2 = source_data['bot_response']
    
        # Example: Printing the variables
        print(f"Variable 1: {variable1}")
        print("------------------------")
        print(f"Variable 2: {variable2}")

# Retrieve data
try:
    results = elastic_func.es_search_for_conv(es_index_name)

    # Process and print results
    for hit in results['hits']['hits']:
        print(hit['_source'])

    # Process into variables
    # process_conversation_results(results)

except Exception as e:
    print(f"Error retrieving data: {e}")
