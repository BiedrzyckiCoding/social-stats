from TikTokApi import TikTokApi, exceptions
import asyncio
import os
import random
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import SessionNotCreatedException
from webdriver_manager.chrome import ChromeDriverManager

# Function to automatically fetch ms_token via a browser load, handling CAPTCHA
def fetch_ms_token():
    print("[DEBUG] Launching browser to fetch ms_token...")

    def make_uc_options():
        opts = uc.ChromeOptions()
        opts.headless = False  # visible browser so CAPTCHA can be solved
        return opts

    # Launch browser (stealth try, fallback to standard)
    try:
        driver = uc.Chrome(options=make_uc_options())
    except SessionNotCreatedException as e:
        print(f"[DEBUG] uc.Chrome failed (likely version mismatch): {e}")
        print("[DEBUG] Falling back to standard Selenium with managed driver...")
        path = ChromeDriverManager().install()
        print(f"[DEBUG] Installed ChromeDriver at: {path}")
        service = Service(path)
        driver = webdriver.Chrome(service=service, options=make_uc_options())

    try:
        driver.get("https://www.tiktok.com/")
        time.sleep(3)
        # Detect possible CAPTCHA by URL or page text
        if "captcha" in driver.current_url.lower() or "verify" in driver.page_source.lower():
            print("[DEBUG] CAPTCHA detected. Please solve it in the browser window.")
            input("Press Enter here after completing the CAPTCHA...")
        # Allow cookies from main site
        time.sleep(2)

        cookie = driver.get_cookie("msToken")
        if not cookie:
            print("[ERROR] msToken cookie not found; ensure TikTok is loaded and you're logged in.")
            raise RuntimeError("msToken cookie not found")

        ms_token = cookie["value"]
        print(f"[DEBUG] Retrieved ms_token (truncated): {ms_token[:12]}...")
        return ms_token
    finally:
        driver.quit()

async def user_example():
    print("[DEBUG] Starting user_example...")

    # Retrieve ms_token from env or fetch automatically
    ms_token = os.environ.get("ms_token")
    if not ms_token:
        ms_token = fetch_ms_token()
    print(f"[DEBUG] Using ms_token: {ms_token[:12]}...")

    # TikTokApi session settings
    browser_choice = os.getenv("TIKTOK_BROWSER", "webkit")
    headless_mode = True
    print(f"[DEBUG] Browser choice: {browser_choice}, headless: {headless_mode}")

    async with TikTokApi() as api:
        # Attempt session creation, retry on bot block
        print("[DEBUG] Creating TikTokApi session...")
        try:
            await api.create_sessions(
                ms_tokens=[ms_token],
                num_sessions=1,
                sleep_after=3,
                browser=browser_choice,
                headless=headless_mode
            )
        except exceptions.EmptyResponseException:
            print("[DEBUG] Empty response (bot detection). Retrying with headless=False & chromium...")
            await api.create_sessions(
                ms_tokens=[ms_token],
                num_sessions=1,
                sleep_after=3,
                browser="chromium",
                headless=False
            )
        print("[DEBUG] Session created.")

        # Fetch user info
        user = api.user("booktalespol")
        delay = random.uniform(2, 3)
        print(f"[DEBUG] Sleeping for {delay:.2f}s before fetching user info...")
        await asyncio.sleep(delay)
        print("[DEBUG] Fetching user info...")
        user_data = await user.info()
        print(f"[DEBUG] User info: {user_data}\n")

        # Fetch videos
        print("[DEBUG] Starting video fetch loop...")
        async for idx, video in enumerate(user.videos(count=30), start=1):
            print(f"[DEBUG] Video {idx}: {video.as_dict}")
            delay = random.uniform(2, 3)
            print(f"[DEBUG] Sleeping for {delay:.2f}s before next video...")
            await asyncio.sleep(delay)

        # Fetch playlists
        print("[DEBUG] Starting playlist fetch loop...")
        async for idx, playlist in enumerate(user.playlists(), start=1):
            print(f"[DEBUG] Playlist {idx}: {playlist}")
            delay = random.uniform(2, 3)
            print(f"[DEBUG] Sleeping for {delay:.2f}s before next playlist...")
            await asyncio.sleep(delay)

if __name__ == "__main__":
    print("[DEBUG] Running user_example...\n")
    asyncio.run(user_example())
