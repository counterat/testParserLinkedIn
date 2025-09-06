import asyncio, time, random
from typing import Literal
from playwright.async_api import Page

from logger.logger import logger
from scraper.recent_activity.selectors import SectionSelectors

async def human_pause(kind: Literal["micro","step","slow"]="step"):
    base = {"micro": 0.25, "step": 0.8, "slow": 1.2}[kind]
    jitter = random.uniform(0.10, 0.40)
    duration = base + jitter
    logger.debug(f"Human-like pause: {duration:.2f}s")
    await asyncio.sleep(duration)
    
async def get_count_of_posts(page: Page):
    count = await page.locator(SectionSelectors.post_selector).count()
    logger.debug(f"Found {count} posts on the page")
    return count
    
async def wait_new_posts(page: Page, prev: int, timeout_ms: int = 3000) -> bool:
    logger.debug(f"Waiting for new posts to appear (prev={prev}, timeout={timeout_ms}ms)")
    t0 = time.time()
    while (time.time() - t0) * 1000 < timeout_ms:
        cur = await get_count_of_posts(page)
        if cur > prev:
            logger.info(f"New posts detected: {cur} (previously {prev})")
            return True
        await asyncio.sleep(0.15)
    logger.debug("No new posts detected within timeout")
    return False


async def scroll(
    page: Page,
    min_posts: int = 10,
    max_posts: int = 10,
    timeout_seconds: int = 60,
    max_idle_iters: int = 4,
    step_ratio: float = 0.6,
) -> int:
    logger.info(f"Starting scroll loop: min_posts={min_posts}, max_posts={max_posts}, "
                f"timeout={timeout_seconds}s, max_idle_iters={max_idle_iters}")
    
    start = time.time()

    try:
        await page.locator(SectionSelectors.post_selector).first.wait_for(timeout=10000)
        logger.info("First post detected on the page")
    except TimeoutError:
        logger.error("Timeout: no posts loaded after 10s")
        return 0

    last_count = await get_count_of_posts(page)
    idle_iters = 0

    while True:
        elapsed = time.time()
        if max_posts <= last_count:
            logger.info(f"Reached max_posts={max_posts}, stopping. Total posts={last_count}")
            return last_count
        if idle_iters >= max_idle_iters and elapsed - start > timeout_seconds:
            logger.warning(f"""Stopping due to idle limit (idle_iters={idle_iters}) and timeout exceeded ({elapsed:.1f}s). Total posts={last_count}""")
            return last_count
        
        logger.debug("Performing page scroll")
        await page.evaluate(f"window.scrollBy(0, document.body.scrollHeight * {step_ratio});")
        await human_pause("slow")

        updated = await wait_new_posts(page, last_count, timeout_ms=3500)
        if updated:
            last_count = await get_count_of_posts(page)
            idle_iters = 0
            continue

        n = await get_count_of_posts(page)
        if n > 0:
            try:
                logger.debug("Scrolling into view of the last visible post")
                await page.locator(SectionSelectors.post_selector).nth(n - 1).scroll_into_view_if_needed()
                await human_pause("slow")
                updated = await wait_new_posts(page, last_count, timeout_ms=2500)
                if updated:
                    last_count = await get_count_of_posts(page)
                    idle_iters = 0
                    continue
            except Exception as e:
                logger.warning(f"scroll_into_view failed: {e}")

        idle_iters += 1
        logger.debug(f"Idle iteration incremented: {idle_iters}")
