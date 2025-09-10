from datetime import datetime
import json
from typing import List

from playwright.async_api import Locator, Page
from config import FILE_FOR_RESULTS
from logger.logger import logger
from parser.comments import parse_counts
from parser.dateformatter import normalize_posted_at
from parser.hashtags import process_hashtags
from person.person import Person
from scraper.base import PipelineBuilder
from scraper.recent_activity.navigator import Navigator
from scraper.recent_activity.schemas import PostSchema
from scraper.recent_activity.scroller import RecentActivityScroller, scroll
from scraper.recent_activity.selectors import SectionSelectors
from session.manager import open_with_storage


#Builder
class RecentActivityPipelineBuilder(PipelineBuilder):
    
    def set_posts(self, posts: List[PostSchema] = []):
        self.posts = posts
        return self
    
    def set_posts_count(self, posts_count = 0):
        self.posts_count = posts_count
        return self
    
    def build(self,*args, **kwargs):
        return RecentActivityPipeline(self.person, self.navigator, self.posts, self.posts_count)

class RecentActivityPipeline:

    def __init__(self, person, navigator, posts, posts_count) -> None:
        self.person : Person = person
        self._navigator = navigator
        self._posts: posts
        self._posts_count = posts_count
        logger.info("Pipeline created")
    
    def _safe_get(self, lst, idx, default=None):
        return lst[idx] if idx < len(lst) else default
    
    async def _all_text_contents(self, lst: List):
        out = []
        for el in lst:
            try:
                out.append(await el.text_content())
            except Exception as e:
                logger.debug(f"text_content failed: {e}",)
                out.append(None)
        return out
    
    async def _get_posted_at(self, lst: List):
        if not lst:
            logger.warning("posted_at list empty")
            return None
        try:
            raw = await lst[0].text_content()
            return normalize_posted_at(raw)
        except Exception as e:
            logger.warning(f"posted_at parse error: {e}")
            return None
    
    async def _comments_count(self, lst: List):
        texts = await self._all_text_contents(lst)
        comments_text = self._safe_get(texts, 0)
        val = parse_counts([comments_text]).get('comments', 0) if comments_text else 0
        logger.debug("comments parsed")
        return val

    async def _reposts_count(self, lst: List):
        texts = await self._all_text_contents(lst)
        reposts_text = self._safe_get(texts, 1)
        val = parse_counts([reposts_text]).get('reposts', 0) if reposts_text else 0
        logger.debug("reposts parsed")
        return val
    
    async def _fetch_mandatory_elements(self, page: Page, post_element: Locator):
        post_id = await post_element.get_attribute("data-urn")
        texts_in_post = await post_element.locator(SectionSelectors.text_selector).all()
        posted_at = await post_element.locator(SectionSelectors.posted_at_selector).all()
        hashtags_elements = await post_element.locator(SectionSelectors.hashtags_selector).all()
        links_elements = await post_element.locator(SectionSelectors.links_selector).all()
        reposts_and_comments_count = await post_element.locator(SectionSelectors.reposts_and_comments_count_selector).all()
        author_names = await post_element.locator(SectionSelectors.author_of_post).all()
        author_of_commented_post = await post_element.locator(SectionSelectors.author_of_commented_content_selector).all()

    
        logger.debug("elements fetched")

        return (
            post_id,
            texts_in_post,
            posted_at,
            hashtags_elements,
            links_elements,
            reposts_and_comments_count,
            author_of_commented_post,
            author_names
        )  
                
    async def _get_only_links(self, lst: List[Locator]):
        links = [el for el in lst if await self._is_link(el)]
        hrefs = []
        for el in links:
            try:
                hrefs.append(await el.get_attribute("href"))
            except Exception as e:
                logger.debug(f"href read failed: {e}")
        return hrefs
        
    async def _is_link(self, locator: Locator):
        child_count = await locator.locator(">*").count()
        return child_count == 0
    
    def _save(self):
        result = {
            "profile_url":self.person.profile_url,
            "posts_count":self._posts_count,
            "created_at":datetime.now().isoformat(),
            "posts":[post.dict() for post in self._posts]
        }
        with open(FILE_FOR_RESULTS, "w", encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        logger.info("results saved")
        
    async def scrape_section(self, max_posts: int, timeout: int, min_posts=10):
        pw, browser, ctx, page = await open_with_storage()
        try:
            section_url = self._navigator.get_url_for_section()
            await page.goto(section_url, wait_until="domcontentloaded")
            scroller = RecentActivityScroller(page)
            self._posts_count = await scroller.scroll(page, max_posts=max_posts, timeout_seconds=timeout, min_posts=min_posts)
            all_posts = await page.locator(SectionSelectors.post_selector).all()
            for post in all_posts:
                
                post_id, texts_in_post, posted_at, hashtags_elements, links_elements, reposts_and_comments_count, author_of_commented_post, author_names = await self._fetch_mandatory_elements(page, post)
                text = await self._all_text_contents(texts_in_post)                
                posted_at = await self._get_posted_at(posted_at)
                reposts_count = await self._reposts_count(reposts_and_comments_count)
                comments_count = await self._comments_count(reposts_and_comments_count)
                hashtags = await self._all_text_contents(hashtags_elements)
                hashtags = process_hashtags(hashtags)
                hrefs_of_links = await self._get_only_links(links_elements)
                author_name = await self._all_text_contents(author_names)
                if len(author_of_commented_post):
                    author_of_commented_post = await self._all_text_contents(author_of_commented_post)
                else:
                    author_of_commented_post = []
                post_processed = PostSchema(
                    post_id=post_id,
                    text=f"".join(text),
                    hashtags=hashtags,
                    posted_at=posted_at,
                    reposts_count=reposts_count,
                    comments_count=comments_count,
                    links=hrefs_of_links,
                    author_name="".join(author_name),
                    author_name_of_commented_content="".join(author_of_commented_post) 
                )
                self._posts.append(post_processed)
                logger.debug("post parsed")
                
        except Exception as e:
            logger.error(f"scrape error: {e}")
            raise
        
        finally:
            await ctx.close()
            await browser.close()
            await pw.stop()
            self._save()


