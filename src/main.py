from fastapi import FastAPI
from routers  import base,data 
from helpers.config import getSettings
from motor.motor_asyncio import AsyncIOMotorClient

settings=getSettings()

app = FastAPI(title=settings.APP_NAME)
@app.on_event("startup")
async def startup():
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)    
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

@app.on_event("shutdown")
async def shutDownSpan():
    app.mongo_conn.close()

app.include_router(base.baseRouter)
app.include_router(data.dataRouter)
