from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Spider
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


class ArchiveSpider(Spider):
    name = 'archive'
    start_urls = []
    custom_settings = {
        'LOG_FILE': 'archive.log',
    }

    def __init__(self, website_str=''):
        self.website = Newspaper.get(website_str.upper(), default='None')
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
            self.logger.info('No link found. Stopping scraper.')
            return

        # if website uses relative url, prepend all links with domain name
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
        title = ''
        body = ''
        date = ''

        titles = response.xpath(
            '//*[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
            website.title_class).getall()
        if (not titles):
            self.logger.warning('No title found for article in {}'.format(
                response.url))
        else:
            title = titles[0].strip()

        # append text from all children nodes into one
        bodies = response.xpath(
            '//div[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
            website.body_class).getall()
        if (not bodies):
            self.logger.warning('No body found for article in {}'.format(
                response.url))
        else:
            bodies = [text.strip() for text in bodies]
            body = ' '.join(bodies)

        if (website.date_class):
            # append text from all children nodes into one
            dates = response.xpath('//*[contains(@class, \'%s\')]/text()' %
                                   website.date_class).getall()
            if (not dates):
                self.logger.warning('No date found for article in {}'.format(
                    response.url))
            else:
                date = dates[0].strip()

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
