import pagination
import re
import requests

from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from typing import Callable
from typing import List
from typing import Match


@dataclass
class Website():
    """
        Holds information on newspaper's structure for scraping.

    Args:
        name name of the newspaper.
        seed_urls URLs to start scraping from.
        base_url base url to use in case of relative urls.
        next_page returns next page to scrape.
        urls seed URLs for scraping.
        target_patterns regular expressions of links to follow during scraping.
        relative_url True if URLs in website are relative, False if they are absolute.
        title_class CSS class of title.
        body_class CSS class of body.
    """
    name: str
    homepage: str
    seed_urls: List[str]
    url_patterns: Match
    relative_url: bool
    title_class: str
    body_class: str
    date_class: str
    favicon: str
    next_button_id: str
    next_request: Callable[[HtmlResponse], Request]


DAWN = Website(
    name='dawn',
    homepage='https://www.dawn.com/',
    seed_urls=['https://www.dawn.com/archive/'],
    url_patterns=re.compile(r'https:\/\/www\.dawn\.com\/news\/[^#]*'),
    relative_url=False,
    title_class='story__title',
    body_class='story__content',
    date_class='story__time',
    favicon='https://www.dawn.com/favicon.ico',
    next_button_id=None,
    next_request=pagination.next_request_dawn)
REUTERS = Website(
    name='reuters',
    homepage='https://www.reuters.com/',
    seed_urls=[
        'https://uk.reuters.com/news/archive/worldnews?view=page&page=1&pageSize=10'
    ],
    url_patterns=re.compile(
        r'(https:\/\/uk\.reuters\.com\/article\/.*)|(\/article\/.*)'),
    relative_url=True,
    title_class='ArticleHeader_headline',
    body_class='StandardArticleBody_body',
    date_class='ArticleHeader_date',
    favicon='https://www.reuters.com/resources/images/favicon.ico',
    next_button_id=None,
    next_request=pagination.next_request_reuters)
PBS = Website(
    name='pbs',
    homepage='https://www.pbs.org/',
    seed_urls=['https://www.pbs.org/newshour/world/page/1'],
    url_patterns=re.compile(
        r'https:\/\/www\.pbs\.org\/newshour\/world\/(?!page).*'),
    relative_url=False,
    title_class='post__title',
    body_class='body-text',
    date_class='post__date',
    favicon='https://www.pbs.org/favicon.ico',
    next_button_id=None,
    next_request=pagination.next_request_pbs)
KHAAMA = Website(
    name='khaama',
    homepage='https://www.khaama.com/',
    seed_urls=['https://www.khaama.com/category/afghanistan/'],
    url_patterns=re.compile(
        r'https:\/\/www\.khaama\.com\/[^\/]*-[^\/]*-[^\/]*\/'),
    relative_url=False,
    title_class='single-title',
    body_class='post-content',
    date_class='single-meta',
    favicon='https://www.khaama.com/favicon.ico',
    next_button_id='load-more',
    next_request=None)

websites = {'DAWN': DAWN, 'KHAAMA': KHAAMA, 'REUTERS': REUTERS, 'PBS': PBS}
