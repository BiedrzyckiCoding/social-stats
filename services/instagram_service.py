import instaloader
from interfaces.platform_interface import PlatformInterface

class InstagramService(PlatformInterface):
    def __init__(self, session_user):
        self.L = instaloader.Instaloader()
        self.L.load_session_from_file(session_user)

    def fetch_stats(self, username: str):
        print(f"\n[Instagram] @{username}")
        try:
            profile = instaloader.Profile.from_username(self.L.context, username)
            print(f"- Followers: {profile.followers}")
            posts = profile.get_posts()
            count = 0
            for post in posts:
                if post.is_video:
                    print(f"- {post.caption[:50]}: {post.video_view_count} views")
                    count += 1
                    if count >= 5:
                        break
        except Exception as e:
            print(f"Error fetching Instagram data for @{username}: {e}")
