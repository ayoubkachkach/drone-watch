import dateparser
import os
import re

import itertools

from ..items import ArticleItem
from django.apps import apps
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from web.models import Article
from web.models import Source
from website import websites
from datetime import datetime


def parse_date(dates):
    dates = [date.strip().split('/') for date in dates]
    dates = [dateparser.parse(date) for date in list(itertools.chain(*dates))]

    for date in dates:
        if date:
            return date
    return None

def parse_article(response):
        spider = response.meta['spider']
        website = response.meta['website']
        title = ''
        body = ''
        date = None

        titles = response.xpath(
            '//*[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
            website.title_class).getall()
        if (not titles):
            spider.logger.warning('No title found for article in {}'.format(
                response.url))
        else:
            title = titles[0].strip()

        # append text from all children nodes into one
        paragraphs = response.xpath(
            '//div[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
            website.body_class).getall()
        if (paragraphs):
            body = '\n'.join(p.strip() for p in paragraphs)
        else:
            spider.logger.warning('No body found for article in {}'.format(
                response.url))
            return

        # append text from all children nodes into one
        dates = response.xpath('//*[contains(@class, \'%s\')]/text()' %
                               website.date_class).getall()

        date = parse_date(dates)

        if (not date):
            spider.logger.warning('No date found for article in {}'.format(
                response.url))
            date = datetime.datetime(1, 1, 1)

        # clean body from javascript escape characters
        body = re.sub(re.compile('\\xad'), '', body)
        body = re.sub(re.compile('\\n'), ' ', body)

        article_item = ArticleItem(
            title=title,
            body=body,
            date_published=date,
            url=response.url,
            source=spider.source)
        yield article_item

class ArchiveSpider(Spider):
    name = 'archive'
    start_urls = []

    # custom_settings = {
    #     'LOG_FILE': 'archive.log',
    # }

    def __init__(self, website_str=''):
        self.website = websites.get(website_str.upper(), None)
        self.page_number = 1
        if (self.website is None):
            raise ValueError(
                'No website {} available. Enter one of the following websites: {}'
                .format(website_str, list(websites.keys())))
        if self.website.next_request is None:
            raise ValueError(
                'Website {} should be run under scraper dynamic_archive_spider: no dynamic pagination here!'
                .format(website_str))

        self.next_request = self.website.next_request
        self.rules = [
            Rule(
                LinkExtractor(allow=self.website.url_patterns),
                callback=parse_article)
        ]
        self.start_urls = self.website.seed_urls
        self.source = Source.objects.get_or_create(
            name=self.website.name,
            homepage=self.website.homepage,
            favicon=self.website.favicon)[0]

    def parse(self, response):
        website = self.website
        # extract all links from current page that respect pattern
        links = set(response.css('a::attr(href)').re(website.url_patterns))
        if (not links):
            self.logger.info('No link found. Stopping scraper.')
            return

        # if website uses relative url, prepend all links with domain name
        if (website.relative_url):
            links = (response.urljoin(link) for link in links if link)

        # only keep unvisited links
        links = (link for link in links if not Article.objects.filter(url=link))

        for link in links:
            yield response.follow(link, callback=parse_article, meta={'spider': self, 'website': website})

        request = self.next_request(self, response)
        # if there is no next page, stop
        if (not request):
            return

        self.page_number +=1
        yield request
