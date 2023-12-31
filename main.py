from pathlib import Path
from datetime import date
import os
import toml
import random
import threading
import logging
import tiktok
import youtube
import instagram

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(account: str, check_lr: bool = False):
    # Load config file
    with open("config.toml", "r") as file:
        config = toml.load(file)

    # Check when the script was last run
    if check_lr == True:
        if config["last run"]["date"] == str(date.today()):
            logger.info("Script already run today. Exiting.")
            return

    # Select a random video
    folder = config[account]["path"]
    video_name = random.choice(os.listdir(folder))
    video = folder + video_name
    logger.info(f"{video} has been chosen. {type(video)}")

    # Get relevant info
    caption = config[account]["caption"]
    tiktok_cookies = config[account]["tiktok_cookies"]
    instagram_uid = config[account]["insta_uid"]
    instagram_pwd = config[account]["insta_pwd"]

    # Create threads for each social media platform
    threads = [
        threading.Thread(target=tiktok.post, args=(video, caption, tiktok_cookies)),
        threading.Thread(
            target=instagram.main, args=(instagram_uid, instagram_pwd, video, caption)
        ),
        threading.Thread(target=youtube.main, args=(video, caption)),
    ]

    # Start and join threads
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # update last used date
    config["last run"]["date"] = str(date.today())
    with open("config.toml", "w") as file:
        toml.dump(config, file)

    # move used video away to prevent reselection
    if not os.path.exists("./used"):
        os.mkdir("./used")

    os.rename(video, f"./used/{video_name}")
    os.rename(f"{video}.jpg", f"./used/{video_name}")

    return


if __name__ == "__main__":
    main("cozycore")
