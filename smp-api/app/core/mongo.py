from pymongo import MongoClient

# MongoDB attributes
mongodb_uri = "mongodb://tonyne:tonyne@localhost:27017/"

client = MongoClient(mongodb_uri)


def get_mongodb(db_name: str):
    return client[db_name]
