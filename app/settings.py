from __future__ import annotations

from starlette.config import Config
from starlette.datastructures import Secret

cfg = Config(".env")

APP_HOST: str = cfg.get("APP_HOST", cast=str)
APP_PORT: int = cfg.get("APP_PORT", cast=int)

OSU_CLIENT_ID: str = cfg("OSU_CLIENT_ID", cast=str)
OSU_CLIENT_SECRET: Secret = cfg("OSU_CLIENT_SECRET", cast=Secret)

# https://docs.python.org/3/library/logging.html#levels
LOG_LEVEL: int = cfg.get("LOG_LEVEL", cast=int)
