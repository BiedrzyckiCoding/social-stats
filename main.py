import sys
import asyncio

import nest_asyncio
from utils.env_loader import load_env
from services.youtube_service import YouTubeService
from services.instagram_service import InstagramService
from services.tiktok_service import TikTokService

nest_asyncio.apply()

# Load environment and initialize services
env = load_env()
youtube = YouTubeService(env["YOUTUBE_API_KEY"])
instagram = InstagramService(env["INSTAGRAM_SESSION"])
tiktok = TikTokService(env["TIKTOK_MS_TOKEN"])

youtube_list = ['@BookTalesPolska', '@BookTalesEnglish', '@BookTalesEsp']
tiktok_list = ['booktalespol', 'booktaleseng', 'booktalesesp']
instagram_list = ['booktalespol', 'booktaleseng', 'booktalesesp']

async def process_tiktok():
    for user in tiktok_list:
        await tiktok.fetch_stats(user)

def run_async_task(coro):
    try:
        # If we're in a notebook or interactive shell
        if "ipykernel" in sys.modules or "idlelib" in sys.modules:
            import nest_asyncio
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(coro)
        else:
            return asyncio.run(coro)
    except RuntimeError as e:
        print(f"Event loop issue: {e}")

def main():
    # print("Fetching YouTube Stats...")
    # for yt in youtube_list:
    #     youtube.fetch_stats(yt)

    # print("\nFetching Instagram Stats...")
    # for ig in instagram_list:
    #     instagram.fetch_stats(ig)

    print("\nFetching TikTok Stats...")
    run_async_task(process_tiktok())

if __name__ == "__main__":
    main()
