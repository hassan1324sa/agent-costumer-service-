from ..vecotrDBInterface import VectorDBInterFace
import logging
from ..vectorDBEnum import DistanceMethodEnums
from qdrant_client import QdrantClient, models
from models.dbSchemes import RetrieveDocs


class QdrantDB(VectorDBInterFace):
    def __init__(self, dbPath: str, distanceMethod: str):
        super().__init__()
        self.client = None
        self.dbPath = dbPath

        if distanceMethod == DistanceMethodEnums.COSINE.value:
            self.distanceMethod = models.Distance.COSINE
        elif distanceMethod == DistanceMethodEnums.DOT.value:
            self.distanceMethod = models.Distance.DOT
        else:
            self.distanceMethod = models.Distance.COSINE 

        self.logger = logging.getLogger(__name__)


    def connect(self):
        self.client = QdrantClient(path=self.dbPath)
        self.logger.info(f"Connected to Qdrant at {self.dbPath}")

    def disconnect(self):
        self.client = None
        self.logger.info("Disconnected from Qdrant")


    def isCollectionExisted(self, collectionName: str) -> bool:
        return self.client.collection_exists(collection_name=collectionName)

    def listAllCollections(self):
        return self.client.get_collections()

    def getCollectionInfo(self, collectionName):
        return self.client.get_collection(collection_name=collectionName)

    def deleteCollection(self, collectionName):
        if self.isCollectionExisted(collectionName):
            self.client.delete_collection(collection_name=collectionName)
            self.logger.info(f"Collection '{collectionName}' deleted.")
            return True
        return False

    def createCollection(self, collectionName: str, embeddingSize: int, doReset: bool = False):
        """
        Create the collection only if it doesn't exist, or reset if requested.
        """
        if doReset:
            self.deleteCollection(collectionName)

        if not self.isCollectionExisted(collectionName):
            self.client.create_collection(
                collection_name=collectionName,
                vectors_config=models.VectorParams(
                    size=embeddingSize,
                    distance=self.distanceMethod
                )
            )
            self.logger.info(f"Collection '{collectionName}' created successfully.")
            return True

        self.logger.info(f"Collection '{collectionName}' already exists.")
        return False


    def insertOne(self, collectionName: str, text: str, vector, metadata=None, recordId=None):
        try:
            self.client.upsert(
                collection_name=collectionName,
                points=[
                    models.PointStruct(
                        id=recordId,
                        vector=vector,
                        payload={"text": text, **(metadata or {})}
                    )
                ]
            )

            self.client.update_collection(
                collection_name=collectionName,
                optimizer_config=models.OptimizersConfigDiff(indexing_threshold=1)
            )

            print(f"✅ Inserted record {recordId} into {collectionName}")
        except Exception as e:
            print(f"❌ Error inserting: {e}")
    def insertMany(self, collectionName, texts, vectors, metadata=None, recordIds=None, batchSize=50):
        if not self.isCollectionExisted(collectionName):
            self.logger.error(f"Cannot insert records: collection '{collectionName}' does not exist.")
            return False

        metadata = metadata or [None] * len(texts)
        recordIds = recordIds or [None] * len(texts)

        try:
            for i in range(0, len(texts), batchSize):
                batchEnd = i + batchSize
                batchTexts = texts[i:batchEnd]
                batchVectors = vectors[i:batchEnd]
                batchMetadata = metadata[i:batchEnd]
                batchRecordIds = recordIds[i:batchEnd]

                batchRecords = [
                    models.Record(
                        id=batchRecordIds[x],
                        vector=batchVectors[x],
                        payload={"text": batchTexts[x], "metadata": batchMetadata[x]}
                    )
                    for x in range(len(batchTexts))
                ]

                self.client.upload_records(collection_name=collectionName, records=batchRecords)

            self.logger.info(f"Inserted {len(texts)} records into '{collectionName}'.")
            return True

        except Exception as e:
            self.logger.error(f"Error while inserting multiple records: {e}")
            return False


    def searchByVector(self, collectionName, vector, limit=5):
        if not self.isCollectionExisted(collectionName):
            self.logger.error(f"Collection '{collectionName}' does not exist.")
            return None

        try:
            results = self.client.search(
                collection_name=collectionName,
                query_vector=vector,
                limit=limit
            )

            if not results:
                return None

            return [
                RetrieveDocs(
                    score=i.score,
                    text=i.payload.get("text", "")
                )
                for i in results
            ]

        except Exception as e:
            self.logger.error(f"Error while searching in '{collectionName}': {e}")
            return None
    
    def deletePoint(self, collectionName, recordId):
        if not self.isCollectionExisted(collectionName):
            self.logger.error(f"Collection '{collectionName}' does not exist.")
            return False

        try:
            self.client.delete(collection_name=collectionName, points_selector=models.PointIdsList(points=[recordId]))
            self.logger.info(f"Deleted record {recordId} from '{collectionName}'.")
            return True
        except Exception as e:
            self.logger.error(f"Error while deleting record {recordId}: {e}")
            return False

