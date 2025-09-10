




class Person:
    
    
    def __init__(self, profile_url:str) -> None:
        self.profile_url = profile_url
        
    async def parse_section(self, min_posts: int, max_posts: int, timeout: int, section = 'recent activity'):
        from scraper.recent_activity.pipeline import RecentActivityPipelineBuilder
        from scraper.recent_activity.navigator import Navigator


    
        if section == 'recent activity':
            builder = RecentActivityPipelineBuilder(self)
            pipeline = builder.set_navigator(Navigator(self)).set_posts().set_posts_count().build()
            await pipeline.scrape_section(max_posts=max_posts, timeout=timeout, min_posts=min_posts)