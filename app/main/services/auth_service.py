import json
import requests

from app.main import schemas
from app.main.core.config import Config
from typing import Any


class AuthService:
    url: str = Config.AUTH_API_URL
    headers: dict = {
        "Content-Type": "application/json",
        "Prefer": "application/json",
        "Api-Key": Config.API_KEY
    }

    def __init__(self):
        pass

    @classmethod
    def get_auth_token(cls, token: str) -> Any:
        res = requests.get(f"{cls.url}/utils/validate-token/{token}", json.dumps({
        }), headers=cls.headers,)
        response = res.json()
        print(f"................................ {response}")
        if res.status_code in [200]:
            return response
        return False

    @classmethod
    def get_user(cls, token: str) -> Any:
        res = requests.get(f"{cls.url}/utils/get_user/{token}", json.dumps({
        }), headers=cls.headers,)
        response = res.json()
        if res.status_code in [200]:
            return response
        return False


auth = AuthService()
