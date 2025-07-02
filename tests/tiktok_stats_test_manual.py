import asyncio
from playwright.async_api import async_playwright
import json

async def login_and_get_cookies():
    async with async_playwright() as p:
        browser = await p.webkit.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.tiktok.com/login")

        print("⚠️ Please log in manually in the browser window.")
        print("✅ Press ENTER here once you’ve completed login...")

        input()  # Wait for manual login

        cookies = await context.cookies()
        with open("tiktok_cookies.json", "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2)

        print("✅ Cookies saved to tiktok_cookies.json")
        await browser.close()

asyncio.run(login_and_get_cookies())
