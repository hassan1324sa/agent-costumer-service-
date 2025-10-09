from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    MONGODB_URL: str
    MONGODB_DATABASE: str
    COHERE_API_KEY:str
    AGENT_SECRET_KEY:str
    VDB_PATH:str
    FASTAPI_URL:str
    BOT_TOKEN:str
    VECTOR_DB_DISTANCE_METHOD:str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

def getSettings():
    return Settings()
