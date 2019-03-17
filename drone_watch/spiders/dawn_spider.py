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


def next_page_dawn(response):
    '''Gives next page given current response for dawn.com'''
    curr_url = response.url
    date_format = '%Y-%m-%d'
    #if in archive root page (i.e. today's page)
    if (curr_url == 'https://www.dawn.com/archive/'):
        prev_day = datetime.today() - timedelta(days=1)
        #return yesterday's archives
        return 'https://www.dawn.com/archive/%s' % prev_day.strftime(
            date_format)

    url_format = r'https:\/\/www.dawn.com\/archive\/(\d\d\d\d-\d\d-\d\d)'
    res = re.search(url_format, curr_url)
    if (not res):
        return None

    #Get match of first parenthesized group in regexp (i.e. date)
    curr_date = res.group(1)
    prev_day = datetime.strptime(curr_date, date_format) - timedelta(days=1)

    return 'https://www.dawn.com/archive/%s' % prev_day.strftime(date_format)


def next_page_reuters(response):
    '''Gives next page given current response from reuters.com'''
    curr_url = response.url
    url_format = r'https:\/\/uk\.reuters\.com\/news\/archive\/worldnews\?view=page&page=(\d+)&pageSize.*'
    res = re.search(url_format, curr_url)
    if (not res):
        return None

    #Get match of first parenthesized group in regexp (i.e. page)
    page = int(res.group(1))
    return 'https://uk.reuters.com/news/archive/worldnews?view=page&page={}&pageSize=10'.format(
        page + 1)


def next_page_pbs(response):
    '''Gives next page given current response from pbs.org'''
    curr_url = response.url
    #if in archive root page (i.e. 1st page)
    if (curr_url == 'https://www.pbs.org/newshour/world'):
        return 'https://www.pbs.org/newshour/world/page/2'

    url_format = r'https:\/\/www\.pbs\.org\/newshour\/world\/page\/(\d*)'
    res = re.search(url_format, curr_url)
    if (not res):
        return None

    #Get match of first parenthesized group in regexp (i.e. page number)
    page = int(res.group(1))
    return 'https://www.pbs.org/newshour/world/page/{}'.format(
        page + 1)


websites = {
    'dawn':
    Newspaper(
        name='dawn',
        seed_urls=['https://www.dawn.com/archive/'],
        url_patterns=re.compile(r'https:\/\/www\.dawn\.com\/news\/[^#]*'),
        relative_url=False,
        title_class='story__title',
        body_class='story__content',
        date_class='story__time',
        next_page=next_page_dawn),
    'reuters':
    Newspaper(
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
        next_page=next_page_reuters),
    'pbs':
    Newspaper(
        name='pbs',
        seed_urls=[
            'https://www.pbs.org/newshour/world/page/1'
        ],
        url_patterns=re.compile(
            r'https:\/\/www\.pbs\.org\/newshour\/world\/(?!page).*'),
        relative_url=True,
        title_class='post__title',
        body_class='body-text',
        date_class='post__date',
        next_page=next_page_pbs)
}


class ArchiveSpider(Spider):
    name = 'archive'
    start_urls = []

    def __init__(self, website_str=''):
        self.website = websites.get(website_str, None)
        self.next_page = self.website.next_page
        self.rules = [
            Rule(
                LinkExtractor(allow=self.website.url_patterns),
                callback=self.parse_article)
        ]
        self.start_urls = self.website.seed_urls

    def parse(self, response):
        website = self.website

        if (not website):
            pass

        # extract all links from current page that respect pattern
        links = set(response.css('a::attr(href)').re(website.url_patterns))
        if (not links):
            return

        #if website uses relative url
        if (website.relative_url):
            links = (response.urljoin(link) for link in links if link)

        for link in links:
            yield response.follow(link, callback=self.parse_article)

        next_page = self.next_page(response)
        # if there is no next page, stop
        if (not next_page):
            return

        yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        website = self.website

        title = ' '.join(
            response.xpath(
                '//*[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
                website.title_class).getall()[0])

        # append text from all children nodes into one
        body = ' '.join(
            response.xpath(
                '//div[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
                website.body_class).getall())

        date = ''
        if(website.date_class):
            # append text from all children nodes into one
            date = response.xpath(
                    '//*[contains(@class, \'%s\')]/text()' %
                    website.date_class).getall()[0]

        # clean body from javascript escape characters
        body = re.sub(re.compile('\\xad'), '', body)
        body = re.sub(re.compile('\\n'), ' ', body)

        content = 'Title: {}\nDate: {}\nBody:\n{}'.format(title, date, body)

        link_title = response.url.split("/")[-1]
        filename = '%s.txt' % link_title
        path = 'articles/{}/'.format(website.name)

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
