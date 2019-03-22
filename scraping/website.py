import requests
from collections import namedtuple
from enum import Enum
import re
import pagination
from typing import Match, List, Callable
from requests import Response
from dataclasses import dataclass


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
    seed_urls: List[str]
    url_patterns: Match
    relative_url: bool
    title_class: str
    body_class: str
    date_class: str
    next_page: Callable[[Response], str]


DAWN = Website(
    name='dawn',
    seed_urls=['https://www.dawn.com/archive/'],
    url_patterns=re.compile(r'https:\/\/www\.dawn\.com\/news\/[^#]*'),
    relative_url=False,
    title_class='story__title',
    body_class='story__content',
    date_class='story__time',
    next_page=pagination.next_page_dawn),
REUTERS = Website(
    name='reuters',
    seed_urls=[
        'https://uk.reuters.com/news/archive/worldnews?view=page&page=1&pageSize=10'
    ],
    url_patterns=re.compile(
        r'(https:\/\/uk\.reuters\.com\/article\/.*)|(\/article\/.*)'),
    relative_url=True,
    title_class='ArticleHeader_headline',
    body_class='StandardArticleBody_body',
    date_class='ArticleHeader_date',
    next_page=pagination.next_page_reuters),
PBS = Website(
    name='pbs',
    seed_urls=['https://www.pbs.org/newshour/world/page/1'],
    url_patterns=re.compile(
        r'https:\/\/www\.pbs\.org\/newshour\/world\/(?!page).*'),
    relative_url=True,
    title_class='post__title',
    body_class='body-text',
    date_class='post__date',
    next_page=pagination.next_page_pbs)

websites = {'DAWN': DAWN, 'REUTERS': REUTERS, 'PBS': PBS}
