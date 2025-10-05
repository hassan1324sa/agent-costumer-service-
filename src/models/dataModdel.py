from .baseDataModel import BaseDataModel
from .dbSchemes import Data
from .enums.dataBaseEunm import DataBaseEnum


class DataModel(BaseDataModel):
    def __init__(self, dbClient:object):
        super().__init__(dbClient)
        self.collection = dbClient[DataBaseEnum.collectionDataEnum.value]
    
    @classmethod
    async def createInstance(cls,dbClient:object):
        instance = cls(dbClient)
        await instance.initCollection()
        return instance
    
    
    async def initCollection(self):
        allCollections = await self.dbClient.list_collection_names()
        if DataBaseEnum.collectionDataEnum.value not in allCollections:
            self.collection = self.dbClient[DataBaseEnum.collectionDataEnum.value]
            indexes = Data.getIndexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    
    async def createData(self,data:Data):
        result = await self.collection.insert_one(data.dict(by_alias=True,exclude_unset=True))
        data.id = result.inserted_id
        return data
    
    async def getDataOrCreateOne(self,dataId:str):
        record = await self.collection.find_one({
            "dataId":dataId
        })
        if record is None:
            data = Data(dataId=dataId)
            data = await self.createData(data)
            return data
        return Data(**record)
    
    async def getAllData(self):
        cursor = self.collection.find({})
        data = await cursor.to_list(length=None)
        return [Data(**item) for item in data]

    async def deleteDataById(self, dataId: str):
        result = await self.collection.delete_one({"dataId": dataId})
        return result.deleted_count > 0

