import os

from pymongo import MongoClient


def setup_mongodb():
    '''Sets up and returns a MongoDB client.'''
    # Retrieve MongoDB connection details from environment variables or use defaults
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://username:password@localhost:27017')
    client = MongoClient(mongodb_uri)

    # Choose the database and collection
    db = client.get_database('urls_scraper')
    collection = db.get_collection('urls')

    return collection
