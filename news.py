import requests
from collections import namedtuple
from enum import Enum
import re
import pagination

class Content:
    """
    Contains information on news articles.
    """

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        """
        Pretty printer for Content objects
        """
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))
        print("BODY:\n {}".format(self.body))


Body = namedtuple('Body', ['name', 'seed_urls', 'url_patterns', 'relative_url', 'title_class', 'date_class', 'body_class', 'next_page'])

class Newspaper(Enum):
    """
        Holds information on newspaper's structure for scraping.

    Args:
        name (str) name of the newspaper.
        seed_urls (list of str) URLs to start scraping from.
        base_url (str) base url to use in case of relative urls.
        next_page (generator of str) returns next page to scrape.
        urls (list of str) seed URLs for scraping.
        target_patterns (list of regexp objects) regular expressions of links to follow during scraping.
        relative_url (bool) True if URLs in website are relative, False if they are absolute.
        title_class (str) CSS class of title.
        body_class (str) CSS class of body.
    """
    DAWN = Body(
        name='dawn',
        seed_urls=['https://www.dawn.com/archive/'],
        url_patterns=re.compile(r'https:\/\/www\.dawn\.com\/news\/[^#]*'),
        relative_url=False,
        title_class='story__title',
        body_class='story__content',
        date_class='story__time',
        next_page=pagination.next_page_dawn),
    REUTERS = Body(
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
    PBS = Body(
        name='pbs',
        seed_urls=['https://www.pbs.org/newshour/world/page/1'],
        url_patterns=re.compile(
            r'https:\/\/www\.pbs\.org\/newshour\/world\/(?!page).*'),
        relative_url=True,
        title_class='post__title',
        body_class='body-text',
        date_class='postdate',
        next_page=pagination.next_page_pbs)

    @classmethod
    def get(cls, member, default=None):
        if(member in cls.__members__):
            return cls[member].value

        return default
