
from playwright.async_api import Page


class Scroller:
    
    def __init__(self, page: Page) -> None:
        self._page = page
    
    async def sroll(self, *args, **kwargs):
        pass
    
    async def _human_pause(self, *args, **kwargs):
        pass