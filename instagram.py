from instagrapi import Client
import os
import dotenv

dotenv.load_dotenv()


def main(path, caption):
    client = Client()

    username, password = os.getenv("insta_uid"), os.getenv("insta_pwd")
    client.login(username, password)

    client.clip_upload(path=path, caption=caption)
