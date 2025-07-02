import asyncio
from TikTokApi import TikTokApi

async def main():
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=None,
            num_sessions=1,
            sleep_after=3,
            browser="webkit",  # more bot-resistant
        )

        user = api.user("booktalespol")
        async for video in user.videos(count=5):
            data = video.as_dict
            print(f"ID: {data.get('id')}")
            print(f"Title: {data.get('desc')}")
            print(f"Views: {data.get('stats', {}).get('playCount')}")
            print("-" * 40)

asyncio.run(main())
