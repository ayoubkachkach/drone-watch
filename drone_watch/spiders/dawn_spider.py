import scrapy
from datetime import datetime, timedelta
import re
import os
from ... import Newspaper

next_url = next_date()
websites = {
    'dawn':Newspaper('dawn', next(next_url), url_patterns=(re.compile(r'https:\/\/www\.dawn\.com\/news\/[^#]*')), absolute_url = True, title_class = 'story__title', body_class = 'story__content')
}

def next_date():
    date_format = '%Y-%m-%d'
    date = datetime.today()
    while (True):
        yield 'https://www.dawn.com/archive/%s' % date.strftime(date_format)
        date = date - timedelta(days=1)


class ArticleSpider(scrapy.Spider):
    name = 'dawn'

    next_url = next_date()

    start_urls = [next(next_url)]

    def __init__(self, website_str=''):


    def parse(self, response):
        LINK_REGEX = #CHANGE
        for link in response.css('a::attr(href)').re(LINK_REGEX):
            yield response.follow(link, callback=self.parse_article)

        yield response.follow(next(self.next_url), callback=self.parse)

    def parse_article(self, response):

        CONTENT_CLASS = #CHANGE
        TITLE_CLASS = #CHANGE

        page = response.url.split("/")[-1]
        filename = '%s.txt' % page

        path = 'articles/dawn/%s' % filename

        title = ''.join(
            response.xpath(
                '//*[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
                TITLE_CLASS).getall()[0])

        #append text from all children nodes into one
        body = ''.join(
            response.xpath(
                '//div[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
                CONTENT_CLASS).getall())
        #clean body from javascript escape characters
        body = re.sub(re.compile('\\xad'), '', body)
        body = re.sub(re.compile('\\n'), ' ', body)

        with open(path, 'w') as f:
            f.write('Title: {}\nBody:\n{}'.format(title, body))


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
