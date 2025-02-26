import logging
import os
import sys
parent_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(os.path.dirname(parent_path))
sys.path.append(root_path)
from config import MONGODB_PROCESSED_COLLECTION
from handlers.mongodb_handler import MongoDBHandler

def get_data():
    documents = []
    try:
        mongodbhandler = MongoDBHandler(MONGODB_PROCESSED_COLLECTION)

        query = {
            'cluster_id': {
                '$exists': True
            },
            'display_document': {
                '$exists': True
            }
        }
        documents = list(mongodbhandler.read_data(query))
    
    except Exception as ex:
        logging.error(f'Error in get_data: {ex}')
    
    return documents