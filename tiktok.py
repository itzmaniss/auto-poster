import time
from playwright.sync_api import sync_playwright, Playwright
import dotenv
import os

dotenv.load_dotenv()


def login(username, password, account):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.tiktok.com/login/phone-or-email/email/?lang=en")
        time.sleep(4)

        # enter username
        page.mouse.move(497, 235)
        page.mouse.click(497, 235)
        page.keyboard.type(username, delay=200)

        # enter password
        page.mouse.move(497, 302)
        page.mouse.click(497, 302)
        page.keyboard.type(password, delay=200)
        page.mouse.move(806, 291)
        page.mouse.click(818, 318)
        time.sleep(1)
        page.mouse.click(818, 318)

        # click login
        page.mouse.move(622, 383)
        page.mouse.click(622, 383)

        # complete captcha
        input("Please complete captcha and press enter to continue")
        time.sleep(3)

        # collect cookies
        context.storage_state(path=f"{account}_state.json")
        time.sleep(2)

        browser.close()


def post(path, caption, storage_state):
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
        with page.expect_file_chooser() as fc_info:
            page.locator('css=button:has-text("Select file")').dblclick()
            file_chooser = fc_info.value
        file_chooser.set_files(path)

        # type in caption
        page.locator("//div[@spellcheck='false']").click()
        page.keyboard.type(caption)
        print("waitiing for upload to finish")
        time.sleep(10)
        print("clicking")

        # page.locator("//div[contains(@class, 'jsx-399018856') and contains(@class, 'btn-post')]//button[contains(., 'Post')]").click()
        page.evaluate('document.querySelector(".btn-post > button").click()')
        print("clicked")
        time.sleep(10)

        browser.close()
