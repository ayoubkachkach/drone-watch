from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Spider
from datetime import datetime, timedelta
import re
import os
from news import Newspaper

def write_safely(path, filename, content):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

    with open(path + filename, 'w') as f:
            f.write(content)

def next_date():
    date_format = '%Y-%m-%d'
    date = datetime.today()
    while (True):
        yield 'https://www.dawn.com/archive/%s' % date.strftime(date_format)
        date = date - timedelta(days=1)

next_url = next_date()
websites = {
    'dawn':
}

class ArticleSpider(Spider):
    name = 'dawn'

    next_url = next_date()

    start_urls = [next(next_url)]

    def __init__(self, website_str=''):
        self.website = websites[website_str]
        self.rules = [Rule(LinkExtractor(allow=self.website.url_patterns), callback=self.parse_article)]
    
    def parse(self, response):
        for link in response.css('a::attr(href)').re(self.website.url_patterns):
            yield response.follow(link, callback=self.parse_article)
        yield response.follow(next(self.next_url), callback=self.parse)

    def parse_article(self, response):
        title = ''.join(
            response.xpath(
                '//*[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
                self.website.title_class).getall()[0])

        #append text from all children nodes into one
        body = ''.join(
            response.xpath(
                '//div[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
                self.website.body_class).getall())

        #clean body from javascript escape characters
        body = re.sub(re.compile('\\xad'), '', body)
        body = re.sub(re.compile('\\n'), ' ', body)
        
        content = 'Title: {}\nBody:\n{}'.format(title, body)

        link_title = response.url.split("/")[-1]
        filename = '%s.txt' % link_title
        path = 'articles/{}/'.format(self.website.name)

        write_safely(path, filename, content)
        


# start_urls = [
#     'https://www.dawn.com/newspaper/front-page/',
#     'https://www.dawn.com/newspaper/back-page/',
#     'https://www.dawn.com/newspaper/national/',
#     'https://www.dawn.com/newspaper/international/',
#     'https://www.dawn.com/newspaper/lahore/',
#     'https://www.dawn.com/newspaper/islamabad/',
#     'https://www.dawn.com/newspaper/peshawar/',
#     'https://www.dawn.com/newspaper/karachi'
# ]
