import os
import shutil
import glob
import asyncio
import logging


async def remove_temp_files_thread(interval: int = 24 * 60):
    """
    Remove temporary files created by the program.
    """
    while True:
        await asyncio.sleep(interval)
        logging.debug("Performing housekeeping tasks...")

        for path in glob.glob("temp/*"):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

        for html_file in glob.glob("static/htmls/*.html"):
            os.remove(html_file)

        logging.info("Housekeeping tasks completed.")
