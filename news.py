import requests

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


class Newspaper:
    """
        Holds information on newspaper's structure for scraping.
    """

    def __init__(self, name, seed_urls, url_patterns, absolute_url, title_class,
                 body_class, next_page):
        """
        Args:
            name (str) name of the newspaper.
            seed_urls (list of str) URLs to start scraping from.
            base_url (str) base url to use in case of relative urls.
            next_page (generator of str) returns next page to scrape.
            urls (list of str) seed URLs for scraping.
            target_patterns (list of regexp objects) regular expressions of links to follow during scraping.
            absolute_url (bool) True if URLs in website are absolute, False if they are relative.
            title_class (str) CSS class of title.
            body_class (str) CSS class of body.
        """
        self.name = name
        self.url_patterns = url_patterns
        self.absolute_url = absolute_url
        self.title_class = title_class
        self.body_class = body_class
        self.next_page = next_page
        self.seed_urls = seed_urls

# from bs4 import BeautifulSoup as BSoup
# import requests
# import re

# URL = 'https://www.dawn.com/'
# LINK_REG_EX = re.compile('https:\/\/www\.dawn\.com\/news\/[^#]*')

# r = requests.get(URL)

# page = BSoup(r.text, features="html.parser")

# for a in page.find_all('a'):
#     link = a.get('href')
#     if link and LINK_REG_EX.match(link):
#         print("Link: {}\nTitle: {}\n".format(link, a.text))
#
