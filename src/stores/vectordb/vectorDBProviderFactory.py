from .providers import QdrantDB
from .vectorDBEnum import VectorDBEnums
from controllers.baseController import BaseController

class VectorDBProviderFactory:
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()

    def create(self, provider: str):
        if provider == VectorDBEnums.QDRANT.value:
            dbPath = self.base_controller.getDatabasePath(dbName=self.config.VECTOR_DB_PATH)

            return QdrantDB(
                dbPath=dbPath,
                distanceMethod=self.config.VECTOR_DB_DISTANCE_METHOD,
            )
        
        return None