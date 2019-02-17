from bs4 import BeautifulSoup as BSoup
import requests
import re

URL = 'https://www.nytimes.com/search/'
# URL = 'https://www.nytimes.com/'
LINK_REG_EX = re.compile('(\/[a-zA-Z0-9\-]*)*\/\d\d\d\d\/\d\d\/\d\d.*')
TITLE_CSS_CLASS = 'css-1lppelv'

r = requests.get(URL)

page = BSoup(r.text, features="html.parser")

for a in page.find_all('a'):
    link = a.get('href')
    title = a.find(True, TITLE_CSS_CLASS)

    if link and LINK_REG_EX.match(link) and title is not None:
        title = title.text
        print("Link: {}\nTitle: {}\n".format(link, title))
 
# URL = 'https://www.nytimes.com/'
# LINK_REG_EX = re.compile('(\/[a-zA-Z0-9\-]*)*\/\d\d\d\d\/\d\d\/\d\d[^#]*')

# r = requests.get(URL)

# page = BSoup(r.text, features="html.parser")

# for a in page.find_all('a'):
#     link = a.get('href')    
#     if link and LINK_REG_EX.match(link):
#         print("Link: {} Title: {}\n".format(link, a.text))
 
