from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME : str

    class Config:
        env_file=".env"
        env_file_encoding = "utf-8"



def getSettings():
    return Settings()