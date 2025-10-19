from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from routers import base, data, booking
from helpers.config import getSettings
from stores.vectordb.providers.QdrantDB import QdrantDB
from stores.vectordb.vectorDBEnum import DistanceMethodEnums
import cohere
from bot.telegramBot import runBot
import asyncio

settings = getSettings()
app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.on_event("startup")
async def startup():
    app.settings = settings

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    app.qdrant = QdrantDB(
        dbPath=settings.VDB_PATH,
        distanceMethod=DistanceMethodEnums.COSINE.value
    )
    app.qdrant.connect()
    app.qdrant.createCollection(collectionName="rag_data", embeddingSize=768)

    app.cohere_client = cohere.Client(settings.COHERE_API_KEY)

    asyncio.create_task(runBot(app))

@app.on_event("shutdown")
async def shutdown():
    app.mongo_conn.close()
    app.qdrant.disconnect()


app.include_router(base.baseRouter)
app.include_router(data.dataRouter)
app.include_router(booking.bookingRouter)
