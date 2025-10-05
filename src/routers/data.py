"""
1 - add data for rag like items or courses or data for rag QA
2 - process data 
"""
from fastapi import FastAPI, APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from controllers.dataController import DataController
from models.dataModdel import DataModel
from models.dbSchemes import Data
from helpers.config import getSettings, Settings
from models import ResponseEnum
import uuid

dataRouter = APIRouter(
    prefix="/api/data", 
)



@dataRouter.post("/add/")
async def addData(request: Request, question: str, answer: str, appSettings: Settings = Depends(getSettings)):
    dbClient = request.app.db_client
    dataModel = await DataModel.createInstance(dbClient=dbClient)
    dataController = DataController()
    try:
        if dataController.validateData(question=question)[0]:
            dataId = str(uuid.uuid4()).replace("-", "")
            dataRecourse = Data(
                question=question,
                answer=answer,
                dataId=dataId
            )
            dataRecord = await dataModel.createData(dataRecourse)
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
        print("Error:", e)
        return JSONResponse(
            content={"signal": ResponseEnum.dataAddedError.value},
            status_code=status.HTTP_400_BAD_REQUEST
        )



@dataRouter.delete("/delete/")
async def deleteData(request: Request, dataId: str, appSettings: Settings = Depends(getSettings)):
    dbClient = request.app.db_client
    dataModel = await DataModel.createInstance(dbClient=dbClient)

    try:
        deleteResult = await dataModel.deleteDataById(dataId)

        if deleteResult:
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
        print("Error:", e)
        return JSONResponse(
            content={"signal": ResponseEnum.dataDeletedError.value},
            status_code=status.HTTP_400_BAD_REQUEST
        )


@dataRouter.get("/all/")
async def getAllData(request: Request, appSettings: Settings = Depends(getSettings)):
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
        else:
            return JSONResponse(
                content={"signal": ResponseEnum.dataNotFound.value, "data": []},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        print("Error:", e)
        return JSONResponse(
            content={"signal": ResponseEnum.dataFetchError.value},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    


@dataRouter.put("/edit/")
async def editData(request: Request, dataId: str, question: str = None, answer: str = None, appSettings: Settings = Depends(getSettings)):
    dbClient = request.app.db_client
    dataModel = await DataModel.createInstance(dbClient=dbClient)

    try:
        if not question and not answer:
            return JSONResponse(
                content={"signal": "noFieldsToUpdate"},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        updateData = {}
        if question:
            updateData["question"] = question
        if answer:
            updateData["answer"] = answer

        updatedRecord = await dataModel.updateDataById(dataId, updateData)

        if updatedRecord:
            return JSONResponse(
                content={
                    "signal": ResponseEnum.dataUpdatedSuccessfully.value,
                    "data": {
                        "dataId": updatedRecord["dataId"],
                        "question": updatedRecord["question"],
                        "answer": updatedRecord["answer"]
                    }
                },
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"signal": ResponseEnum.dataNotFound.value},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        print("Error:", e)
        return JSONResponse(
            content={"signal": ResponseEnum.dataUpdateError.value},
            status_code=status.HTTP_400_BAD_REQUEST
        )

