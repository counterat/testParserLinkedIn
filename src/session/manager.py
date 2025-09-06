from pathlib import Path
from playwright.async_api import async_playwright

STORAGE = Path("out/storage.json")

async def open_with_storage(
    timezone_id="Europe/Sofia",
    locale="en-US",
    viewport={"width": 1366, "height": 900},
    channel="chrome",
    headless=False,
):
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(channel=channel, headless=headless)

    ctx = await browser.new_context(
        storage_state=str(STORAGE),
        viewport=viewport,
        locale=locale,
        timezone_id=timezone_id,
    )
    page = await ctx.new_page()
    return pw, browser, ctx, page
