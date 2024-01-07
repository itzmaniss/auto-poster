import time
from playwright.sync_api import sync_playwright
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def login(username: str, password: str, account: str) -> str:
    path = f"{account}_tiktok_state.json"
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.tiktok.com/login/phone-or-email/email/?lang=en")
        time.sleep(4)

        # enter username
        logger.info("Entering Username")
        page.mouse.move(497, 235)
        page.mouse.click(497, 235)
        page.keyboard.type(username, delay=200)

        # enter password
        logger.info("Entering Password")
        page.mouse.move(497, 302)
        page.mouse.click(497, 302)
        page.keyboard.type(password, delay=200)
        page.mouse.move(806, 291)
        page.mouse.click(818, 318)
        time.sleep(1)
        page.mouse.click(818, 318)

        # click login
        logger.info("Logging in")
        page.mouse.move(622, 383)
        page.mouse.click(622, 383)

        # complete captcha
        logger.info("Waiting for user to run captcha")
        input("Please complete captcha and press enter to continue")
        time.sleep(3)

        # collect cookies
        logger.info("Collecting all cookies to use for posting")
        context.storage_state(path=path)
        time.sleep(2)

        browser.close()


def post(path, caption, storage_state):
    logger.info("Opening up tiktok website")
    with sync_playwright() as p:
        # launch the browser
        browser = p.firefox.launch()
        context = browser.new_context(
            storage_state=storage_state, **p.devices["Desktop Firefox"]
        )
        page = context.new_page()

        # goto the posting page
        page.goto("https://www.tiktok.com/creator#/upload?scene=creator_center")
        time.sleep(2)

        # upload video file
        logger.info("Uploading the video file")
        with page.expect_file_chooser() as fc_info:
            page.locator('css=button:has-text("Select file")').dblclick()
            file_chooser = fc_info.value
        file_chooser.set_files(path)
        time.sleep(3)

        # type in caption
        logger.info("Typing in the caption")
        page.locator("//div[@spellcheck='false']").click()
        page.keyboard.type(caption)
        print("waitiing for upload to finish")
        time.sleep(10)

        # press the post button
        page.evaluate('document.querySelector(".btn-post > button").click()')
        logger.info("Posting the video")
        time.sleep(10)

        browser.close()
