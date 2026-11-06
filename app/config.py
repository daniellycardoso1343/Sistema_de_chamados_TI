import os 
from dotenv import load_dotenv

load_dotenv()


secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise RuntimeError("Defina SECRET_KEY no arquivo .env")


database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("Defina DATABASE_URL no arquivo .env")


class Config:
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = database_url