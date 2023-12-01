from pymongo import MongoClient
from app.core.config import settings
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDB:
    client: MongoClient = None

    @staticmethod
    def initialize():
        try:
            MongoDB.client = MongoClient(settings.MONGO_URL)
            return MongoDB.client
        except Exception as e:
            logger.error("Error connecting to the database", exc_info=True)

    @staticmethod
    def get_database():
        try:
            if MongoDB.client is None:
                MongoDB.initialize()
            return MongoDB.client[settings.MONGO_DB_NAME]
        except Exception as e:
            logger.error("Error getting the database", exc_info=True)

    @staticmethod
    def close():
        if MongoDB.client is not None:
            MongoDB.client.close()
            MongoDB.client = None
