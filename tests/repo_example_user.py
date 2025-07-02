from TikTokApi import TikTokApi
import asyncio
import os

ms_token = os.environ.get(
    "ms_token", None
)  # set your own ms_token, think it might need to have visited a profile


async def user_example():
    async with TikTokApi() as api:
        await api.create_sessions(headless=False, ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        user = api.user("booktalespol")
        user_data = await user.info()
        print(f"[DEBUG] User info: {user_data}")

        async for video in user.videos(count=30):
            data = video.as_dict

            # extract only the fields you want
            filtered = {
                "description": data.get("desc"),
                "author_name": data.get("author", {}).get("nickname"),
                "play_count": data.get("stats", {}).get("playCount"),
                "like_count": data.get("stats", {}).get("diggCount"),
                "share_count": data.get("stats", {}).get("shareCount"),
                "comment_count": data.get("stats", {}).get("commentCount"),
            }

            print(filtered)

if __name__ == "__main__":
    asyncio.run(user_example())