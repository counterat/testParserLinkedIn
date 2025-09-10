
from playwright.async_api import Page

from person.person import Person
from scraper.recent_activity.navigator import Navigator


#Factory
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
        

#Builder
class PipelineBuilder:
    
    def __init__(self, person) -> None:
        self.person : Person = person
    
    def set_navigator(self, navigator):
        self._navigator = navigator #Navigator(self.person)
        return self
    
    def build(self,*args, **kwargs):
        pass
