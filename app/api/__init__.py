from __future__ import annotations

import asyncio
import logging
import os

from fastapi import Request
from fastapi import Response
from fastapi.applications import FastAPI
from fastapi.responses import PlainTextResponse
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware

from . import middlewares
from app import tasks
from app.api import v1

PATHS = [
    ".data",
    ".data/thumbnails",
    ".data/temp",
    ".data/temp/htmls",
    ".data/temp/osz",
]

TASKS = [
    tasks.remove_temp_files_thread,
]

futures: list[asyncio.Future] = []


def ensure_data_folders():
    """
    Ensure and create data folders if they don't exist.
    """
    for path in PATHS:
        if not os.path.exists(path):
            logging.info(f"Creating {path} directory...")
            os.mkdir(path)


def home_page(request: Request) -> Response:
    """Home page for API"""
    return PlainTextResponse("Thumbnail API is working!", 200)


def init_middlewares(app: FastAPI) -> None:
    """Initialize the app's middlewares."""
    app.add_middleware(PrometheusMiddleware)
    app.add_middleware(middlewares.ProcessTimeMiddleware)


def init_events(app: FastAPI) -> None:
    """Setup the app's startup & shutdown events."""

    @app.on_event("startup")
    async def on_startup() -> None:
        ensure_data_folders()
        for task in TASKS:
            futures.append(asyncio.ensure_future(task()))

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        ...


def init_endpoints(app: FastAPI) -> None:
    """Initialize the app's endpoints."""
    app.include_router(v1.router)

    app.add_route("/metrics", handle_metrics)
    app.add_route("/", home_page)


def init_api() -> FastAPI:
    """Initialize the API."""
    app = FastAPI()

    init_middlewares(app)
    init_events(app)
    init_endpoints(app)

    return app


asgi_app = init_api()
