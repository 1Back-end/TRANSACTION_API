import json
import requests
from app.main import schemas
from app.main.core.config import Config


class AuthService:
    url: str = Config.AUTH_API_URL
    headers: dict = {
        "Content-Type": "application/json",
        "Prefer": "application/json",
        "Api-Key": Config.API_KEY
    }

    def __init__(self):
        pass

    # @staticmethod

