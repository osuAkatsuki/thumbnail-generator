import os

PATHS = [
    ".data",
    ".data/thumbnails",
    ".data/temp",
    ".data/temp/htmls",
    ".data/temp/osz",
]


def ensure_data_folders():
    """
    Ensure and create data folders if they don't exist.
    """
    for path in PATHS:
        if not os.path.exists(path):
            os.mkdir(path)
