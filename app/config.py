import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "ISO27001-Chatbot"
    API_VERSION: str = "v1"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"

    # Clé de chiffrement des données
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY")

    # Clé JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Base de données
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()

DEBUG = os.getenv("DEBUG", "False") == "True"