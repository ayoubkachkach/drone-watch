import scrapy

from ..items import ArticleItem
from .archive_spider import parse_article
from django.apps import apps
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from selenium import webdriver
from web.models import Article
from web.models import Source
from website import websites
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scrapy.http import TextResponse
import time

def get_suffix_size(a, b):
    a_idx = len(a) - 1
    b_idx = len(b) - 1
    size = 0
    
    while a_idx >= 0 and b_idx >= 0:
        if a[a_idx] != b[b_idx]:
            break
        size += 1
        a_idx -= 1
        b_idx -= 1

    return size

class DynamicArchiveSpider(Spider):
    name = 'dynamic_archive'
    start_urls = []

    # custom_settings = {
    #     'LOG_FILE': 'archive.log',
    # }

    def __init__(self, website_str='', start_url=''):
        self.website = websites.get(website_str.upper(), None)
        self.page_number = 1
        if self.website is None:
            raise ValueError(
                'No website {} available. Enter one of the following websites: {}'
                .format(website_str, list(websites.keys())))
        if self.website.next_request is not None:
            raise ValueError(
                'Website {} should be run under scraper archive_spider: dynamic pagination required!'
                .format(website_str))
        self.driver = webdriver.Firefox()
        self.rules = [
            Rule(
                LinkExtractor(allow=self.website.url_patterns),
                callback=parse_article)
        ]
        self.start_urls = self.website.seed_urls
        if(start_url):
            self.start_urls = [start_url]
        self.source = Source.objects.get_or_create(
            name=self.website.name,
            homepage=self.website.homepage,
            favicon=self.website.favicon)[0]

    def parse(self, response):
        self.driver.get(response.url)
        website = self.website
        while True:
            if self.page_number > 10000:
                break
            try:
                prefix_size = 0
                next = self.driver.find_element_by_id(website.next_button_id)
                next.click()
                time.sleep(5)
                sel_response = TextResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
                if(prefix_size == 0):
                    suffix_size = get_suffix_size(response.css('a::attr(href)').re(website.url_patterns), sel_response.css('a::attr(href)').re(website.url_patterns))
                # extract all links from current page that respect pattern. Remove common links found previously.
                links = sel_response.css('a::attr(href)').re(website.url_patterns)[prefix_size:-suffix_size]
                prefix_size += len(links)
                links = set(links)
                if (not links):
                    self.logger.info('No link found. Stopping scraper.')
                    return
                self.page_number += 1
                # if website uses relative url, prepend all links with domain name
                if (website.relative_url):
                    links = (response.urljoin(link) for link in links if link)

                # only keep unvisited links
                links = (link for link in links if not Article.objects.filter(url=link))

                for link in links:
                    yield response.follow(link, callback=parse_article, meta={'spider': self, 'website': website}, priority=1)
            except Exception as e:
                break
        driver.close()
        driver.quit()


