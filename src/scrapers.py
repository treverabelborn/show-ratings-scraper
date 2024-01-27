from bs4 import BeautifulSoup, Tag, ResultSet
from .models import TvShow

TRAILERS_CDN_URL_BASE = 'https://link.theplatform.com/s/NGweTC/media/'


def scrape_all_shows(soup: BeautifulSoup) -> list[TvShow]:
    shows_container: Tag = soup.find('div', class_='discovery-tiles__wrap')
    shows_tiles: ResultSet[Tag] = shows_container.find_all('div', recursive=False)
    shows = [scrape_show(tile) for tile in shows_tiles]

    return shows

def scrape_show(tag: Tag) -> TvShow:
    parent = tag.find(class_='js-tile-link').select_one('tile-dynamic')
    thumbnail_url = parent.find('rt-img')['src']
    show_info = parent.find(attrs={"data-track": "scores"})
    trailer_url = None if (parent.button is None) else f'{TRAILERS_CDN_URL_BASE}{parent.button["data-public-id"]}'
    title = show_info.span.string.replace('\n', '').strip()
    ratings = show_info.select_one('score-pairs-deprecated')
    critic_rating = ratings['criticsscore']
    audience_rating = ratings['audiencescore']

    return TvShow(
        title=title,
        thumbnail_url=thumbnail_url,
        trailer_url=trailer_url,
        critic_rating=critic_rating,
        audience_rating=audience_rating
    )