from __future__ import annotations

import logging

from app import settings

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s %(message)s",
)


def main() -> int:

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
