from __future__ import annotations

import logging

import uvicorn

from app import settings

try:
    __import__("uvloop").install()
except ImportError:
    pass

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s %(message)s",
)


def main() -> int:
    # run the server
    uvicorn.run(
        "app.api:asgi_app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        server_header=False,
        date_header=False,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
