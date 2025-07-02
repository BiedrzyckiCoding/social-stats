from TikTokApi import TikTokApi
import asyncio
import random

async def user_example():
    print("[DEBUG] Initializing TikTokApi client using full mobile API (no ms_token, no proxy)...")
    # Instantiate the API client directly (avoid context manager to skip browser attributes)
    api = TikTokApi()
    try:
        print("[DEBUG] TikTokApi client ready.")

        username = "booktalespol"
        print(f"[DEBUG] Fetching user '{username}'...")
        user = api.user(username)

        count = 30
        print(f"[DEBUG] Retrieving up to {count} videos for '{username}'...")
        videos = []
        async for video in user.videos(count=count):
            videos.append(video)
        print(f"[DEBUG] Retrieved {len(videos)} videos.")

        for idx, video in enumerate(videos, start=1):
            data = video.as_dict
            stats = data.get("stats", {})
            print(
                f"[DEBUG] Video {idx}: id={data.get('id')}, "
                f"views={stats.get('play_count')}, "
                f"likes={stats.get('digg_count')}, "
                f"shares={stats.get('share_count')}, "
                f"comments={stats.get('comment_count')}"
            )
    finally:
        print("[DEBUG] Closing TikTokApi client...")
        await api.close()

if __name__ == "__main__":
    print("[DEBUG] Running mobile-API user_example without ms_token and proxy...\n")
    asyncio.run(user_example())