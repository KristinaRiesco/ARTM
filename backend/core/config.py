from dotenv import load_dotenv
import os

#load environment variables from .env file

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'site.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

