#!/usr/bin/env python3

import os
from elasticsearch import Elasticsearch
from datetime import datetime

import common_func

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = script_directory + '/config.yaml'
variables = common_func.load_variables_from_yaml(file_path)


# Connect to Elasticsearch
es_host = 'localhost'
es_port = 9200
es_username = variables['es_username']
es_password = variables['es_password']

es = Elasticsearch(
        [
            {
                'host':str(es_host),
                'port':int(es_port),
                'scheme': variables['es_scheme']
            }
        ],
        basic_auth=(str(es_username), str(es_password)),
        verify_certs=False
)

""" Check es connection """
def es_conn_check():
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Could not connect to Elasticsearch")
        exit()

""" We want to store a stream and qa for ML training"""
def es_index_create(es_index_name):
    if not es.indices.exists(index=es_index_name):
        try:
            res = es.indices.create(es_index_name)
            print(f"Index created with result: {res['result']}")
        except Exception as e:
            print(f"Error creating Index: {e}")
            exit()

""" Stores conversation data in Elasticsearch."""
def es_store_conv(es_index_name, bot_response, bot_response_current):
    timestamp = datetime.now()
    conversation_data = {
        'timestamp': timestamp,
        'bot_response': bot_response,
        'bot_response_current': bot_response_current
    }
    try:
        res = es.index(index=es_index_name, document=conversation_data)
        es.indices.refresh(index=es_index_name)
        print(f"Document indexed with result: {res['result']}")
    except Exception as e:
        print(f"Error indexing document: {e}")

"""   """
def es_get_conv(es_index_name):
    try:
        res = es.get(index=es_index_name, id=1)
        if res['found']:
           print(f"Document found: {res['_source']}")
           return res
        else:
           print("Document not found")
    except Exception as e:
        print(f"Error retrieving document: {e}")

"""   """
# Define the default index and query
query = {
    "query": {
        "match_all": {} # Or any other query
    }
}

def es_search_for_conv(es_index_name, es_query=query):
    try:
        res = es.search(index=es_index_name, body=es_query)
        print(f"Got {res['hits']['total']['value']} hits:")

        return res
    except Exception as e:
        print(f"Error searching documents: {e}")
