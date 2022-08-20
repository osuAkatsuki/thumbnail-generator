import logging
from app import config

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s %(message)s",
)


def main() -> int:

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
