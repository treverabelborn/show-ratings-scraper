import requests
from bs4 import BeautifulSoup
import io
import csv
import boto3
from .models import TvShow
from .scrapers import scrape_all_shows

SRC_URL = 'https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:netflix~sort:popular?page=5'
OUTPUT_BUCKET = 'show-ratings-scraper-output'
OUTPUT_NAME = 'test_run.csv'


def lambda_handler(event, context):
    page = requests.get(SRC_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    scraped_shows: list[TvShow] = scrape_all_shows(soup)
    shows_fields = list(scraped_shows[0].keys())

    output_stream = io.StringIO()
    writer = csv.DictWriter(output_stream, fieldnames=shows_fields)
    writer.writeheader()
    writer.writerows(scraped_shows)
    csv_string = output_stream.getvalue()
    client = boto3.client('s3')
    client.put_object(Body=csv_string, Bucket=OUTPUT_BUCKET, Key=OUTPUT_NAME)

    print(f'Successfully wrote csv output at {OUTPUT_NAME}')