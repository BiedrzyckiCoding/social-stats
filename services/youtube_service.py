from googleapiclient.discovery import build
from interfaces.platform_interface import PlatformInterface

class YouTubeService(PlatformInterface):
    def __init__(self, api_key):
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def resolve_channel_id(self, identifier):
        if identifier.startswith("UC"):
            return identifier
        elif identifier.startswith("@"):
            try:
                response = self.youtube.search().list(
                    part="snippet",
                    q=identifier,
                    type="channel",
                    maxResults=1
                ).execute()
                return response["items"][0]["snippet"]["channelId"]
            except Exception as e:
                print(f"Error resolving handle {identifier}: {e}")
        return None

    def fetch_stats(self, username: str):
        channel_id = self.resolve_channel_id(username)
        if not channel_id:
            return
        try:
            response = self.youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=10,
                order='date'
            ).execute()
            print(f"\n[YouTube] Channel: {channel_id}")
            for item in response['items']:
                video_id = item['id'].get('videoId')
                title = item['snippet']['title']
                if video_id:
                    stats = self.youtube.videos().list(part='statistics', id=video_id).execute()
                    views = stats['items'][0]['statistics'].get('viewCount', '0')
                    print(f"- {title}: {views} views")
        except Exception as e:
            print(f"Error fetching videos for channel {channel_id}: {e}")
