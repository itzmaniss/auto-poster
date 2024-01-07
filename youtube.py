from playwright.sync_api import sync_playwright
import logging
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def post(path, caption, storage_state):
    logger.info("Opening up youtube website")
    path = Path(path)
    with sync_playwright() as p:
        # launch the browser
        browser = p.firefox.launch()
        context = browser.new_context(
            storage_state=storage_state, **p.devices["Desktop Firefox"]
        )
        page = context.new_page()

        page.goto("https://studio.youtube.com/channel/")
        page.locator("text=Create").click()
        page.locator("text=Upload videos").click()

        with page.expect_file_chooser() as fc_info:
            page.locator("text=SELECT FILES").click()
            file_chooser = fc_info.value
        file_chooser.set_files(path)
        time.sleep(3)

        page.get_by_label(
            "Add a title that describes your video (type @ to mention a channel)"
        ).fill(caption)
        time.sleep(2)

        page.get_by_label(
            "Tell viewers about your video (type @ to mention a channel)"
        ).fill(caption)

        for i in range(3):
            page.get_by_role("button", name="Next").click()

        page.locator(
            'tp-yt-paper-radio-button[aria-checked="false"][name="PUBLIC"]'
        ).check()

        page.get_by_role("button", name="Publish").click()
        

        browser.close()
