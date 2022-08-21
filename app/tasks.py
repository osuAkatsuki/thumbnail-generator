import os
import shutil
import glob
import asyncio
import logging

TEMP_PATHS = [
    ".data/temp/htmls",
    ".data/temp/osz",
]


async def remove_temp_files_thread(interval: int = 24 * 60):
    """
    Remove temporary files created by the program.
    """
    while True:
        await asyncio.sleep(interval)
        logging.debug("Performing housekeeping tasks...")

        for path in TEMP_PATHS:
            for file in glob.glob(f"{path}/*"):
                if os.path.isdir(file):
                    shutil.rmtree(file)
                else:
                    os.remove(file)

        logging.info("Housekeeping tasks completed.")
