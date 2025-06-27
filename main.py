import os
import requests
from googleapiclient.discovery import build
from dotenv import load_dotenv
from TikTokApi import TikTokApi
import instaloader
import asyncio

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize APIs
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
L = instaloader.Instaloader()

# Lists of channels/users
youtube_list = ['@BookTalesPolska', '@BookTalesEnglish', '@BookTalesEsp']
tiktok_list = ['booktalespol', 'booktaleseng', 'booktalesesp']
instagram_list = ['booktalespol', 'booktaleseng', 'booktalesesp']

def resolve_channel_id(identifier):
    if identifier.startswith("UC"):
        return identifier
    elif identifier.startswith("@"):
        try:
            response = youtube.search().list(
                part="snippet",
                q=identifier,
                type="channel",
                maxResults=1
            ).execute()
            return response["items"][0]["snippet"]["channelId"]
        except Exception as e:
            print(f"Error resolving handle {identifier}: {e}")
            return None
    else:
        print(f"Invalid identifier format: {identifier}")
        return None

def fetch_youtube_videos(channel_id):
    try:
        response = youtube.search().list(
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
                stats = youtube.videos().list(part='statistics', id=video_id).execute()
                view_count = stats['items'][0]['statistics'].get('viewCount', '0')
                print(f"- {title}: {view_count} views")
    except Exception as e:
        print(f"Error fetching videos for channel {channel_id}: {e}")

async def fetch_tiktok_stats(username):
    print(f"\n[TikTok] @{username}")
    try:
        api = TikTokApi()
        user = api.user(username)
        count = 0
        async for video in user.videos():
            desc = video.desc if video.desc else "(no description)"
            views = video.stats.play_count
            print(f"- {desc[:50]}: {views} views")
            count += 1
            if count >= 5:
                break
    except Exception as e:
        print(f"Error fetching TikTok data for @{username}: {e}")

def fetch_instagram_stats(username):
    print(f"\n[Instagram] @{username}")
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        print(f"- Followers: {profile.followers}")

        posts = profile.get_posts()
        count = 0
        for post in posts:
            if post.is_video:
                print(f"- {post.title[:50]}: {post.video_view_count} views")
                count += 1
            if count >= 5:
                break
    except Exception as e:
        print(f"Error fetching Instagram data for @{username}: {e}")

# Process YouTube
print("Fetching YouTube Stats...")
for yt in youtube_list:
    resolved_id = resolve_channel_id(yt)
    if resolved_id:
        fetch_youtube_videos(resolved_id)

# TikTok (use asyncio for each user)
print("\nFetching TikTok Stats...")
for tk in tiktok_list:
    asyncio.run(fetch_tiktok_stats(tk))

# Process Instagram
print("\nFetching Instagram Stats...")
for ig in instagram_list:
    fetch_instagram_stats(ig)
