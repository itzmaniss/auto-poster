from datetime import date
from pathlib import Path
import os
import toml
import random
import threading
import logging
import tiktok
import youtube
import instagram
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():

    # get account
    account = sys.argv[1]

    # Load config file
    with open("config.toml", "r") as file:
        config = toml.load(file)

    # Select a random video
    folder = Path(config[account]["path"])
    video_name = random.choice(os.listdir(folder))
    video = folder.joinpath(video_name)
    logger.info(f"{video} has been chosen.")

    # Get relevant info
    caption = config[account]["caption"]
    storage_state = Path(config[account]["storage_state"])
    
    # create the threads
    threads = (threading.Thread(target=tiktok.post, args=(video, caption, storage_state,)),
               threading.Thread(target=instagram.post, args=(video, caption, storage_state,)),
               threading.Thread(target=youtube.post, args=(video, caption, storage_state,)))

    # start and join threads
    logger.info("Starting Threads")
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()      
    logger.info("Threads have been joined")    

    logger.info("Updating last used date")
    config[account]["last_run"] = str(date.today())
    with open("config.toml", "w") as file:
        toml.dump(config, file)

    # move used video away to prevent reselection
    if not os.path.exists("./used"):
        logger.info("Creating a used folder for used videos")
        os.mkdir("./used")

    logger.info("Moving used video to Used folder")
    video.rename(f"./used/{video_name}")

if __name__ == "__main__":
    main()