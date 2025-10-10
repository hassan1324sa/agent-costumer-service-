from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    MONGODB_URL: str
    MONGODB_DATABASE: str
    COHERE_API_KEY:str
    VDB_PATH:str
    FASTAPI_URL:str
    BOT_TOKEN:str
    VECTOR_DB_DISTANCE_METHOD:str
    AGENTOPS_API_KEY:str
    LLM_ROUTER:str
    LLM_FAQ_BOOKING:str
    LLM_TEMP:float

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

def getSettings():
    return Settings()
