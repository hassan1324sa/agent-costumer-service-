from fastapi import FastAPI
from routers  import base,data 
from helpers.config import getSettings,Settings

Settings=getSettings()

app = FastAPI(title=Settings.APP_NAME)


app.include_router(base.baseRouter)
app.include_router(data.dataRouter)
