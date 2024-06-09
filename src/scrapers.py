import requests
from bs4 import BeautifulSoup, Tag, ResultSet
from .models import TvShow


TOMATOES_URL = 'https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:netflix~sort:popular'
TRAILERS_CDN_URL_BASE = 'https://link.theplatform.com/s/NGweTC/media/'


def scrape_rotten_tomatoes() -> list[TvShow]:
    page = requests.get(TOMATOES_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    shows_container: Tag = soup.find('div', class_='discovery-tiles__wrap')
    shows_tiles: ResultSet[Tag] = shows_container.find_all('div', recursive=False)
    shows = [scrape_one_show(tile) for tile in shows_tiles]

    return shows
    
def scrape_one_show(tag: Tag) -> TvShow:
    parent = tag.find(class_='js-tile-link').select_one('tile-dynamic')
    thumbnail_url = parent.find('rt-img')['src']
    show_info = parent.find(attrs={"data-track": "scores"})
    trailer_url = None if (parent.button is None) else f'{TRAILERS_CDN_URL_BASE}{parent.button["data-public-id"]}'
    title = show_info.span.string.replace('\n', '').strip()
    ratings = show_info.select_one('score-pairs-deprecated')
    critic_rating = ratings.find(attrs={"slot": "criticsScore"}).text
    audience_rating = ratings.find(attrs={"slot": "audienceScore"}).text

    return TvShow(
        title=title,
        thumbnail_url=thumbnail_url,
        trailer_url=trailer_url,
        critic_rating=critic_rating,
        audience_rating=audience_rating
    )