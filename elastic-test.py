#!/usr/bin/env python3

from elasticsearch import Elasticsearch
from datetime import datetime
    
# Connect to Elasticsearch
es_host = 'localhost'
es_port = 9200
es_username = 'elastic'
es_password = ''

es = Elasticsearch(
        [
            {
                'host':str(es_host), 
                'port':int(es_port),
                'scheme': "https"
            }
        ],
        basic_auth=(str(es_username), str(es_password)),
        verify_certs=False
)
    
# Check connection
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")
    exit()
    
# Define index name
index_name = "conversations_stream"
    
# Create index if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)
    
def store_conversation(user_input, bot_response):
    """Stores conversation data in Elasticsearch."""
    timestamp = datetime.now()
    conversation_data = {
        'timestamp': timestamp,
        'user_input': user_input,
        'bot_response': bot_response
    }
    es.index(index=index_name, document=conversation_data)
    es.indices.refresh(index=index_name)

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
store_conversation("Hello, how are you?", "I am doing well, thank you for asking.")
store_conversation("What is the weather like today?", "The weather is sunny with a high of 25 degrees Celsius.")
    
print("Conversations stored successfully.")

# Define the index and query
query = {
    "query": {
        "match_all": {} # Or any other query
    }
}

# Retrieve data
try:
    results = es.search(index=index_name, body=query)

    # Process and print results
    for hit in results['hits']['hits']:
        print(hit['_source'])

    # Process into variables
    process_conversation_results(results)

except Exception as e:
    print(f"Error retrieving data: {e}")
