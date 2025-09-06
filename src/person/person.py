


class Person:
    
    
    def __init__(self, profile_url:str) -> None:
        self.profile_url = profile_url
        
    async def parse_section(self, min_posts: int, max_posts: int, timeout: int, section = 'recent activity'):
        from scraper.recent_activity.pipeline import Pipeline

        pipeline = Pipeline(self)
        if section == 'recent activity':
            await pipeline.scrape_section(max_posts=max_posts, timeout=timeout, min_posts=min_posts)