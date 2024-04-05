import os
from pydantic_settings import BaseSettings
from typing import Optional


def get_secret(secret_name, default):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return secret_file.read().strip()
    except IOError:
        return os.getenv(secret_name, default)


class ConfigClass(BaseSettings):
    SECRET_KEY: str = get_secret("SECRET_KEY", '9JKIDSoTJTTkGeecMPkLH-BpeFvE5pJi_Wb0Q9H1iPouMJ0')
    ALGORITHM: str = get_secret("ALGORITHM", 'HS256')

    ADMIN_KEY: str = get_secret("ADMIN_KEY", "EpursaKey2024!")
    API_KEY: str = get_secret("API_KEY", "UQcuyktZo23jmD6KsQPh5A")
    ADMIN_USERNAME: str = get_secret("ADMIN_USERNAME", "epursa")
    ADMIN_PASSWORD: str = get_secret("ADMIN_PASSWORD", "hlz5L1yB45g")

    # 60 minutes * 24 hours * 355 days = 365 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(get_secret("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 365))

    SQLALCHEMY_DATABASE_URL: str = get_secret("SQLALCHEMY_DATABASE_URL",
                                              'postgresql://postgres:KmLus48*usT23@localhost:5432'
                                              '/Tradly')

    SQLALCHEMY_POOL_SIZE: int = 100
    SQLALCHEMY_MAX_OVERFLOW: int = 0
    SQLALCHEMY_POOL_TIMEOUT: int = 30
    SQLALCHEMY_POOL_RECYCLE: int = get_secret("SQLALCHEMY_POOL_RECYCLE", 3600)
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": SQLALCHEMY_POOL_RECYCLE,
    }

    MINIO_URL: Optional[str] = get_secret("MINIO_URL", "files.epursa.com")
    MINIO_KEY: Optional[str] = get_secret("MINIO_ACCESS_KEY", "RRqw+Q7KXpLpLiOPwWl0jshEzbP5cBEskc5s6slfyBo=")
    MINIO_SECRET: Optional[str] = get_secret("MINIO_SECRET_KEY",
                                             "KXpD0n0LRRqZfHoskTjDe6SMqcANAkflmmfCFyfGXN7r9AE2o/4pOht"
                                             "+n1jjogmfCFyfGXD0n0N7r9AEDa0kpxfiw==")
    MINIO_BUCKET: str = get_secret("MINIO_BUCKET", "develop")
    MINIO_SECURE: bool = True

    PREFERRED_LANGUAGE: str = get_secret("PREFERRED_LANGUAGE", 'fr')

    API_STR: str = get_secret("API_STR", "/api/v1/transaction")

    PROJECT_NAME: str = get_secret("PROJECT_NAME", "EPURSA TRANSACTION API")
    PROJECT_VERSION: str = get_secret("PROJECT_VERSION", "1.0.0")

    REDIS_HOST: str = get_secret("REDIS_HOST", "localhost")  # redis_develop
    REDIS_PORT: int = get_secret("REDIS_PORT", 6379)
    REDIS_DB: int = get_secret("REDIS_DB", 2)
    REDIS_CHARSET: str = get_secret("REDIS_CHARSET", "UTF-8")
    REDIS_DECODE_RESPONSES: bool = get_secret("REDIS_DECODE_RESPONSES", True)

    LOCAL: bool = os.getenv("LOCAL", True)

    class Config:
        case_sensitive = True


Config = ConfigClass()