import re
from typing import Optional, Dict, List

def parse_counts(parts: List[str]) -> Dict[str, Optional[int]]:
    result = {"comments": None, "reposts": None}
    if not parts:
        return result

    for raw in parts:
        txt = raw.strip().lower()

        m = re.search(r"(\d+)\s*(\w+)", txt)
        if not m:
            continue
        num = int(m.group(1))
        word = m.group(2)

        if word.startswith("comment"): 
            result["comments"] = num
        elif word.startswith("repost"):  
            result["reposts"] = num

    return result
