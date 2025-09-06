from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class PostSchema(BaseModel):
    post_id: str
    author_name: str = ""
    author_name_of_commented_content: Optional[str]
    posted_at: str = datetime.now()
    text: str
    hashtags: List[str] = []
    links: List[str] = []
    reposts_count: int = 0
    comments_count: int = 0