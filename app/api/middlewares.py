from __future__ import annotations

import time

from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    # TODO: can i replace this with prometheus middleware's timing?

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        if request.url.path == "/metrics":
            return await call_next(request)

        start = time.perf_counter_ns()
        response = await call_next(request)
        end = time.perf_counter_ns()

        response.headers["process-time"] = str((end - start) / 1_000_000)  # ns -> ms
        return response
