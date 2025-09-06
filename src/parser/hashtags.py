from typing import List


def process_hashtags(lst: List[str]):
    return [s.replace("hashtag", "") for s in lst]
    