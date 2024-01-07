from playwright.sync_api import sync_playwright
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFileDialog
import toml
import os

def get_folder():
    app = QApplication([])  # Create a PyQt application
    folder = QFileDialog.getExistingDirectory(None, "Select Folder", options=QFileDialog.ShowDirsOnly)
    return folder

def login():
    # check for config file
    if not os.path.exists(Path("./config.toml")):
        os.mkdir(Path("./config.toml"))

    name = input("Enter name for account: ")
    path = Path(f"./{name}_state.json")
    config_path = Path("./config.toml")
    folder = get_folder()

    with sync_playwright() as p:
        # start up browser
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.instagram.com/accounts/login/")
        print("Press Save info after logging in!")
        input("Press enter once you have logged into instagram")
        page.goto("https://www.tiktok.com/login/phone-or-email/email/?lang=en")
        input("Press enter once you have logged into tiktok")
        page.goto("https://www.youtube.com/")
        input("Press enter once you have logged into youtube")

        context.storage_state(path=path)

    with config_path.open(mode="r") as f:
        config = toml.load(f)

    config[name] = {}
    config[name]["last_run"] = ""
    config[name]["path"] = str(folder)
    config[name]["storage_state"] = str(path).lower()
    config[name]["caption"] = input("Enter your default caption: ")

    with config_path.open(mode="w") as f:
        toml.dump(config, f)


if __name__ == "__main__":
    login()
