import requests
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
from enum import Enum


class Platform(Enum):
    Netflix = 1
    Hulu = 2
    AppleTv = 3
    Max = 4
    Disney = 5

class TvShow(TypedDict):
    title: str
    thumbnail_url: str
    # platform: Platform
    critic_rating: int
    audience_rating: int

def get_tv_show(tag: Tag) -> TvShow:
    parent = tag.find(class_='js-tile-link').select_one('tile-dynamic')
    thumbnail_url = parent.find('rt-img')['src']
    show_info = parent.find(attrs={"data-track": "scores"})
    title = show_info.span.string.replace('\n', '').strip()
    scores = show_info.select_one('score-pairs-deprecated')
    critic_rating = scores['criticsscore']
    audience_rating = scores['audiencescore']

    return TvShow(title=title, thumbnail_url=thumbnail_url, critic_rating=critic_rating, audience_rating=audience_rating)


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    url = 'https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:netflix~sort:popular?page=5'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    show_tiles = soup.find('div', class_='discovery-tiles__wrap').find_all('div', recursive=False)

    shows = [get_tv_show(tile) for tile in show_tiles]
    return shows
