from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routers import base, data, booking
from helpers.config import getSettings

settings = getSettings()

app = FastAPI(title=settings.APP_NAME)

@app.on_event("startup")
async def startup():
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

@app.on_event("shutdown")
async def shutdown():
    app.mongo_conn.close()



app.include_router(base.baseRouter)
app.include_router(data.dataRouter)
app.include_router(booking.bookingRouter)
