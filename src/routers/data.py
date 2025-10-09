from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from controllers.dataController import DataController
from models.dataModdel import DataModel
from models.dbSchemes import Data
from helpers.config import getSettings, Settings
from models import ResponseEnum
import uuid


dataRouter = APIRouter(prefix="/api/data")


@dataRouter.post("/add/")
async def addData(request: Request, question: str, answer: str, appSettings: Settings = Depends(getSettings)):
    dbClient = request.app.db_client
    dataModel = await DataModel.createInstance(dbClient=dbClient)
    dataController = DataController()

    try:
        if not dataController.validateData(question=question)[0]:
            return JSONResponse(
                content={"signal": "invalidData"},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        dataId = str(uuid.uuid4()).replace("-", "")
        dataRecourse = Data(
            question=question,
            answer=answer,
            dataId=dataId
        )

        dataRecord = await dataModel.createData(dataRecourse)

        text_to_embed = f"Q: {question}\nA: {answer}"

        co = request.app.cohere_client
        response = co.embed(
            model="embed-multilingual-v3.0",
            texts=[text_to_embed],
            input_type="search_document"
        )
        vector = response.embeddings[0]

        qdrant = request.app.qdrant
        qdrant.insertOne(
            collectionName="rag_data",
            text=text_to_embed,
            vector=vector,
            metadata={"dataId": dataId},
            recordId=dataId
        )

        return JSONResponse(
            content={
                "signal": ResponseEnum.dataAddedSuccessfully.value,
                "data": {
                    "dataId": dataId,
                    "question": dataRecord.question,
                    "answer": dataRecord.answer
                }
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return JSONResponse(
            content={"signal": ResponseEnum.dataAddedError.value},
            status_code=status.HTTP_400_BAD_REQUEST
        )


@dataRouter.delete("/delete/")
async def deleteData(request: Request, dataId: str):
    dbClient = request.app.db_client
    dataModel = await DataModel.createInstance(dbClient=dbClient)
    qdrant = request.app.qdrant

    try:
        deleteResult = await dataModel.deleteDataById(dataId)

        if deleteResult:
            qdrant.deletePoint(collectionName="rag_data", recordId=dataId)

            return JSONResponse(
                content={"signal": ResponseEnum.dataDeletedSuccessfully.value},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"signal": ResponseEnum.dataNotFound.value},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        return JSONResponse(
            content={"signal": ResponseEnum.dataDeletedError.value},
            status_code=status.HTTP_400_BAD_REQUEST
        )


@dataRouter.get("/all/")
async def getAllData(request: Request):
    dbClient = request.app.db_client
    dataModel = await DataModel.createInstance(dbClient=dbClient)

    try:
        all_data = await dataModel.getAllData()

        if all_data:
            data_list = [
                {
                    "dataId": d.dataId,
                    "question": d.question,
                    "answer": d.answer
                }
                for d in all_data
            ]
            return JSONResponse(
                content={
                    "signal": ResponseEnum.dataFetchedSuccessfully.value,
                    "data": data_list
                },
                status_code=status.HTTP_200_OK
            )

        return JSONResponse(
            content={"signal": ResponseEnum.dataNotFound.value, "data": []},
            status_code=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return JSONResponse(
            content={"signal": ResponseEnum.dataFetchError.value},
            status_code=status.HTTP_400_BAD_REQUEST
        )
