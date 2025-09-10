
from logging import Logger
from typing import List
from playwright.async_api import Locator, Page

from person.person import Person
from scraper.recent_activity.navigator import Navigator


#Creational - Factory
class Scroller:
    
    def __init__(self, page: Page) -> None:
        self._page = page
    
    async def sroll(self, *args, **kwargs):
        pass
    
    async def _human_pause(self, *args, **kwargs):
        pass
    
class ScrollerFactory:
    
    @staticmethod
    def create_recent_activity_scroller(page: Page):
        from scraper.recent_activity.scroller import RecentActivityScroller
        return RecentActivityScroller(page)
        

#Creational - Builder
class PipelineBuilder:
    
    def __init__(self, person) -> None:
        self.person : Person = person
    
    def set_navigator(self, navigator):
        self._navigator = navigator #Navigator(self.person)
        return self
    
    def build(self,*args, **kwargs):
        pass

#Structural - Adapter 
class LinkedinTextAdapter:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        
    async def get_text(self, lst: List[Locator], response_type: "string" | "lst" = "string"):

        out = "" if response_type == "string" else []
        for el in lst:
            try:
                if response_type == "string":
                    out += await el.text_content()
                else:
                    out.append(await el.text_content())
            except Exception as e:
                self.logger.debug(f"text_content failed: {e}",)
        return out

