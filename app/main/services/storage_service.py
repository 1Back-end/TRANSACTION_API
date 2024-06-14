import requests
from typing import Any, List
import json

from app.main.core.config import Config


class StorageService:
    url: str = Config.STORAGE_API_URL
    headers: dict = {
        "Content-Type": "application/json",
        "Prefer": "application/json",
        "Api-Key": Config.API_KEY
    }

    def __init__(self):
        pass

    @classmethod
    def get_storage_uuid(cls, article_storage_uuids: List[str]) -> Any:
        res = requests.post(f"{cls.url}/utils/get_storage_uuid", json.dumps({
            'article_storage_uuids': article_storage_uuids,
            'api_key': Config.API_KEY,
        }), headers=cls.headers)
        response = res.json()
        print(f"...............storage image:{response}")
        if res.status_code in [200]:
            return response
        return False

    @classmethod
    def get_storages(cls, storage_uuids: List[str]):
        res = requests.post(f"{cls.url}/utils/get_storages", json.dumps({
            'storage_uuids': storage_uuids,
            'api_key': Config.API_KEY,
        }), headers=cls.headers)
        response = res.json()
        print(f"...............image:{response}")
        if res.status_code in [200]:
            print("====response====", response)
            return response
        return False


storage = StorageService()
