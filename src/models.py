from typing import TypedDict, Optional
from enum import Enum


class Platform(Enum):
    Netflix = 1
    Hulu = 2
    AppleTv = 3
    Max = 4
    Disney = 5


class TvShow(TypedDict):
    title: str
    thumbnail_url: Optional[str]
    trailer_url: str
    # platform: Platform
    critic_rating: int
    audience_rating: int