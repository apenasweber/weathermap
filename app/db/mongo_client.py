from pymongo import MongoClient
from app.core.config import settings


class MongoDB:
    client: MongoClient = None

    @staticmethod
    def initialize():
        MongoDB.client = MongoClient(settings.MONGO_URL)
        return MongoDB.client

    @staticmethod
    def get_database():
        if MongoDB.client is None:
            MongoDB.initialize()
        return MongoDB.client[settings.MONGO_DB_NAME]

    @staticmethod
    def close():
        if MongoDB.client is not None:
            MongoDB.client.close()
            MongoDB.client = None
