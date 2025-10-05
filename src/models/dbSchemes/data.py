from pydantic import BaseModel,Field,field_validator
from typing import Optional
from bson.objectid import ObjectId


class Data(BaseModel):
    id:Optional[ObjectId] = Field(None,alias="_id")
    dataId:str = Field(...,min_length=1)
    question:str = Field(...,min_length=3)
    answer:str = Field(...,min_length=3)
    
    @field_validator("dataId")
    def validateDataId(cls,value):
        if not value.isalnum():
            raise ValueError("data id must be alphanumeric")
        return value

    class Config:
        arbitrary_types_allowed=True
        allow_population_by_field_name = True

    @classmethod
    def getIndexes(cls):
        return [
            {
                "key":[("dataId",1)],
                "name":"dataIdIndex1",
                "unique":True,
            }
        ]

