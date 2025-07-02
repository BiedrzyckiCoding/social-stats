from TikTokApi import TikTokApi
from interfaces.platform_interface import PlatformInterface
import asyncio

class TikTokService(PlatformInterface):
    def __init__(self, ms_token=None):
        self.ms_token = ms_token

    async def fetch_stats(self, username: str):
        print(f"\n[TikTok] @{username}")
        try:
            async with TikTokApi(ms_token=self.ms_token) as api:
                await api.create_sessions()
                user = api.user(username)
                async for video in user.videos(count=5):
                    desc = video.desc or "(no description)"
                    views = video.stats.play_count
                    print(f"- {desc[:50]}: {views} views")
        except Exception as e:
            print(f"Error fetching TikTok data for @{username}: {e}")
