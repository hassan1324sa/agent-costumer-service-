from abc import abstractmethod,ABC
from typing import List

class VectorDBInterFace(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def isCollectionExisted(self,collectionName:str)->bool:
        pass

    @abstractmethod
    def listAllCollections(self)->List:
        pass

    @abstractmethod
    def getCollectionInfo(self,collectionName:str)->dict:
        pass

    @abstractmethod
    def deleteCollection(self,collectionName:str):
        pass

    @abstractmethod
    def createCollection(self,collectionName:str,embeddingSize:int,doReset:bool=False):
        pass

    @abstractmethod
    def insertOne(self,collectionName:str,text:str,vector:list,metadata:dict=None,recordId:str=None):
        pass
    
    @abstractmethod
    def insertMany(self,collectionName:str,texts:str,vector:list,metadata:dict=None,recordIds:str=None,batchSize:int=50):
        pass

    def searchByVector(self, collectionName: str, vector: list, limit: int)->List:
        pass


