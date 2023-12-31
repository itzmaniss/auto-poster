from instagrapi import Client
import os
import dotenv


def main(username, password, path, caption):
    client = Client()

    client.login(username, password)

    client.clip_upload(path=path, caption=caption)
