import time
from playwright.sync_api import sync_playwright
import dotenv
import os

dotenv.load_dotenv()

def login():
    with sync_playwright() as p:
        username = os.getenv("tiktok_uid")
        password = os.getenv("tiktok_pwd")

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

        #click login
        page.mouse.move(622, 383)
        page.mouse.click(622, 383)

        input("Please complete captcha and press enter to continue")
        time.sleep(3)

        # collect cookies
        storage = context.storage_state(path="state.json")

        time.sleep(2)

        browser.close()

def post():
    with sync_playwright() as p:

        browser = p.firefox.launch(headless=False)
        context = browser.new_context(storage_state= "state.json")
        page = context.new_page()

        page.goto("https://www.tiktok.com/creator-center/upload?from=upload")
        time.sleep(10)

        browser.close()