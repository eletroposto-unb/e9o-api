from click import password_option
from pydantic import BaseSettings

class Settings(BaseSettings):
    db_connect_url: str
    firestore_key: str
    firebase_file: str
    class Config:
        env_file = ".env"

settings = Settings()