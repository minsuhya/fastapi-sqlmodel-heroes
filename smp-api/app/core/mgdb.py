from loguru import logger
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

# MongoDB attributes
mongodb_uri = "mongodb://tonyne:tonyne@localhost:27017/"
db_name = "tutorial"

client = MongoClient(mongodb_uri)

# check connection
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command("ismaster")
    # init database
    client.drop_database(db_name)
except ConnectionFailure:
    logger.error("MongoDB Server not available")
    client = None


def get_mongodb() -> Database:
    return client[db_name]
