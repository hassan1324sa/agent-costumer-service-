"""
1 - add data for rag like items or courses or data for rag QA
2 - process data 
"""
from fastapi import FastAPI,APIRouter,Depends,UploadFile,status ,Request
from fastapi.responses import JSONResponse
from helpers.config import getSettings,Settings
from models import ResponseEnum

dataRouter = APIRouter(
    prefix="/api/data", 
)


@dataRouter.post("/upload/")
async def upload(request:Request,question:str,answer:str,appSettings:Settings=Depends(getSettings)):
    print(question)
    return JSONResponse(content={"signal":ResponseEnum.dataAddedSuccessfully.value},status_code=status.HTTP_200_OK)