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

def next_page_dawn(curr_url):
    date_format = '%Y-%m-%d'
    #if in archive root page (i.e. today's page)
    if(curr_url == 'https://www.dawn.com/archive/'):
        prev_day = datetime.today() - timedelta(days = 1)
        return 'https://www.dawn.com/archive/%s' % prev_day.strftime(date_format)

    url_format = r'https:\/\/www.dawn.com\/archive\/(\d\d\d\d-\d\d-\d\d)'
    res = re.search(url_format, curr_url)
    if(not res):
        return None
        #raise ValueError('Given url does not match format', url_format, curr_url)

    #Get match of first parenthesized group in regexp (i.e. date) 
    curr_date = res.group(1)
    prev_day = datetime.strptime(curr_date, date_format) - timedelta(days = 1)
    
    return 'https://www.dawn.com/archive/%s' % prev_day.strftime(date_format)

websites = {
    'dawn': Newspaper(
        name='dawn', 
        seed_urls=['https://www.dawn.com/archive/'], 
        url_patterns=re.compile(r'https:\/\/www\.dawn\.com\/news\/[^#]*'), 
        absolute_url = True, 
        title_class = 'story__title', 
        body_class = 'story__content', 
        next_page=next_page_dawn
    )
}

class ArchiveSpider(Spider):
    name = 'archive'
    start_urls = []
    def __init__(self, website_str=''):
        self.website = websites.get(website_str, None)
        self.next_page = self.website.next_page
        self.rules = [Rule(LinkExtractor(allow=self.website.url_patterns), callback=self.parse_article)]
        self.start_urls = self.website.seed_urls

    def parse(self, response):
        if(not self.website):
            pass

        # extract all links from current page that respect pattern
        links = response.css('a::attr(href)').re(self.website.url_patterns)
        # if no links found, stop crawling
        if(not links):
            return

        for link in links:
            yield response.follow(link, callback=self.parse_article)
        
        next_page = self.next_page(response.url)
        # if there is no next page
        if(not next_page):
            return

        yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        title = ''.join(
            response.xpath(
                '//*[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
                self.website.title_class).getall()[0])

        # append text from all children nodes into one
        body = ''.join(
            response.xpath(
                '//div[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
                self.website.body_class).getall())

        # clean body from javascript escape characters
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
