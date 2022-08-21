from __future__ import annotations

from starlette.config import Config
from starlette.datastructures import Secret

cfg = Config(".env")

OSU_CLIENT_ID = cfg("OSU_CLIENT_ID", cast=str)
OSU_CLIENT_SECRET = cfg("OSU_CLIENT_SECRET", cast=Secret)

# https://docs.python.org/3/library/logging.html#levels
LOG_LEVEL = cfg.get("LOG_LEVEL", cast=int)
