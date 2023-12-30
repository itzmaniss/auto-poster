from requests import get, post
import os
from dotenv import load_dotenv

load_dotenv()

meta_app_id = os.getenv("meta_app_id")


def login():

    scope = "business_management,pages_read_engagement,pages_show_list,instagram_basic,instagram_content_publish"

    login_url = "https://www.facebook.com/dialog/oauth?"\
        f"app_id={meta_app_id}"\
        f"&scope={scope}"\
        f"&client_id={meta_app_id}"\
        "&display=page"\
        "&extras={{setup:{{channel:IG_API_ONBOARDING}}}}"\
        "&redirect_uri=https://127.0.0.1:5000/success"\
        "&response_type=code"
        
    token = get(login_url)
    return token.url

def post(video):
    with open("caption.txt", "r") as file:
        caption = file.read()
    url = f"https://graph.facebook.com/v18.0/17841400008460056/media?media_type=REELS&video_url={video}&caption={caption}"
    