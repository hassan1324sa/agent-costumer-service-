from fastapi import FastAPI,APIRouter,Depends
from helpers.config import getSettings,Settings

baseRouter = APIRouter(
    prefix="/api", 
)


@baseRouter.get("/")
async def welcome(appSettings:Settings=Depends(getSettings)):

    return{
        "name":appSettings.APP_NAME
    }
