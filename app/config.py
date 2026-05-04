from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DEBUG = os.getenv("DEBUG", "False") == "True"
    DATABASE_URL = os.getenv("DATABASE_URI", "mysql+pymysql://dev:dev@localhost/library")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:5001")

settings = Settings()