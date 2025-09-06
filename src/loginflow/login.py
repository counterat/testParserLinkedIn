import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError
from config import URL_FOR_LOGIN

OUT = Path("out"); OUT.mkdir(exist_ok=True)

async def login_and_save(timezone_id="Europe/Sofia", locale="en-US", viewport={"width": 1366, "height": 900}, channel="chrome"):
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            channel=channel,
            headless=False,
            viewport=viewport,
            locale=locale,
            timezone_id=timezone_id,
            slow_mo=120,
        )
        try:
            await ctx.clear_cookies()
        except Exception:
            pass

        page = await ctx.new_page()
        await page.goto(URL_FOR_LOGIN, wait_until="domcontentloaded")

        print("Log in in LinkedIn With Bare Hands Now (2FA, Captcha, ...).")
        try:
            await page.wait_for_url("**/feed/**", timeout=180_000)
        except TimeoutError:
            pass

        await ctx.storage_state(path=str(OUT / "storage.json"))
        print("✅ storage.json saved")

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(login_and_save())
