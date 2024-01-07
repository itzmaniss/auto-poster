from playwright.sync_api import sync_playwright
from pathlib import Path
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def post(path, caption, storage_state):
    logger.info("Opening up instagram website")
    path = Path(path)
    with sync_playwright() as p:
        # launch the browser
        browser = p.firefox.launch()
        context = browser.new_context(
            storage_state=storage_state, **p.devices["Desktop Firefox"]
        )
        page = context.new_page()
        page.goto("https://www.instagram.com/")

        # start posting process
        logging.info("starting to post the video")
        page.get_by_label("New Post").click()

        # upload the file
        logger.info("Uploading the video file")
        with page.expect_file_chooser() as fc_info:
            page.get_by_role("button", name="Select from computer").click()
            file_chooser = fc_info.value
        file_chooser.set_files(path)
        time.sleep(3)

        # skip the reel editing portion
        for i in range(2):
            page.get_by_role("button", name="Next").click()

        # writing caption
        logging.info("writing caption")
        page.get_by_label("Write a caption...").fill(caption)

        # share the reel
        page.get_by_role("button", name="Share").click()
        logging.info("waiting for reel to be shared!")

        page.wait_for_selector("text=Reel shared")
        logging.info("reel shared")

        browser.close()
