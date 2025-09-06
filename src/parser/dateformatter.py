import re
from datetime import datetime, timedelta, timezone
from typing import Optional, Iterable, Union

REL_PATTERNS = [
    r"(?P<num>\d+)\s*(?P<unit>s|sec|m|min|h|d|w|mo|y)\b",
    r"(?P<num>\d+)\s*(?P<unit>second|seconds|minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)\b",

]

def _unit_to_delta(num: int, unit: str) -> Optional[timedelta]:
    u = unit.lower()

    if u in ("s", "sec"):                     return timedelta(seconds=num)
    if u in ("m", "min"):                     return timedelta(minutes=num)
    if u == "h":                              return timedelta(hours=num)
    if u == "d":                              return timedelta(days=num)
    if u == "w":                              return timedelta(weeks=num)
    if u == "mo":                             return timedelta(days=30 * num)  
    if u == "y":                              return timedelta(days=365 * num)  

    if u in ("second", "seconds"):            return timedelta(seconds=num)
    if u in ("minute", "minutes"):            return timedelta(minutes=num)
    if u in ("hour", "hours"):                return timedelta(hours=num)
    if u in ("day", "days"):                  return timedelta(days=num)
    if u in ("week", "weeks"):                return timedelta(weeks=num)
    if u in ("month", "months"):              return timedelta(days=30 * num)
    if u in ("year", "years"):                return timedelta(days=365 * num)


    return None

def _clean_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r"(•|edited|visible to anyone.*|видно всем.*)", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def normalize_posted_at(rel: Optional[Union[str, Iterable[str]]],
                        now: Optional[datetime] = None) -> Optional[str]:

    if rel is None:
        return None

    if isinstance(rel, (list, tuple)):
        rel = " ".join(str(x) for x in rel)

    rel = str(rel).strip()
    if not rel:
        return None

    if (rel[:4].isdigit() and "T" in rel) or re.match(r"^\d{4}-\d{2}-\d{2}T", rel):
        try:
            dt = datetime.fromisoformat(rel.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).isoformat()
        except Exception:
            pass

    t = _clean_text(rel)

    t = re.sub(r"\b(ago|назад)\b", " ", t).strip()

    for pat in REL_PATTERNS:
        m = re.search(pat, t)
        if m:
            num = int(m.group("num"))
            unit = m.group("unit")
            delta = _unit_to_delta(num, unit)
            if delta:
                base = now or datetime.now(timezone.utc)
                return (base - delta).isoformat()

    return None
