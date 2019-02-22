import requests
import scrapers.crawler

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

class Website:
    """
    Contains information on website structure.
    """

    def __init__(self, name, url, target_pattern, absolute_url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.target_pattern = target_pattern
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag


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