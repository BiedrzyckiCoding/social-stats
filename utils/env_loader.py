from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    return {
        "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY"),
        "TIKTOK_MS_TOKEN": os.getenv("TIKTOK_MS_TOKEN"),
        "INSTAGRAM_SESSION": os.getenv("INSTAGRAM_SESSION", "booktalesesp")
    }
