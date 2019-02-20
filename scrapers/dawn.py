import requests
from bs4 import BeautifulSoup

class Crawler:
    


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