import re

from datetime import datetime
from datetime import timedelta
from scrapy import Request, FormRequest


def next_request_dawn(spider, response):
    '''Gives next page given current response for dawn.com'''
    curr_url = response.url
    date_format = '%Y-%m-%d'
    #if in archive root page (i.e. today's page)
    if (curr_url == 'https://www.dawn.com/archive/'):
        prev_day = datetime.today() - timedelta(days=1)
        #return yesterday's archives
        next_page = 'https://www.dawn.com/archive/%s' % prev_day.strftime(
            date_format)
        return Request(next_page, callback=spider.parse)

    url_format = r'https:\/\/www.dawn.com\/archive\/(\d\d\d\d-\d\d-\d\d)'
    res = re.search(url_format, curr_url)
    if (not res):
        return None

    #Get match of first parenthesized group in regexp (i.e. date)
    curr_date = res.group(1)
    prev_day = datetime.strptime(curr_date, date_format) - timedelta(days=1)
    next_page = 'https://www.dawn.com/archive/%s' % prev_day.strftime(
        date_format)

    return Request(next_page, callback=spider.parse)


def next_request_reuters(spider, response):
    '''Gives next page given current response from reuters.com'''
    curr_url = response.url
    url_format = r'https:\/\/uk\.reuters\.com\/news\/archive\/worldnews\?view=page&page=(\d+)&pageSize.*'
    res = re.search(url_format, curr_url)
    if (not res):
        return None

    #Get match of first parenthesized group in regexp (i.e. page)
    page = int(res.group(1))
    next_page = 'https://uk.reuters.com/news/archive/worldnews?view=page&page={}&pageSize=10'.format(
        page + 1)

    return Request(next_page, callback=spider.parse)


def next_request_pbs(spider, response):
    '''Gives next page given current response from pbs.org'''
    curr_url = response.url
    #if in archive root page (i.e. 1st page)
    if (curr_url == 'https://www.pbs.org/newshour/world'):
        next_page = 'https://www.pbs.org/newshour/world/page/2'
        return Request(next_page, callback=spider.parse)

    url_format = r'https:\/\/www\.pbs\.org\/newshour\/world\/page\/(\d*)'
    res = re.search(url_format, curr_url)
    if (not res):
        return None

    #Get match of first parenthesized group in regexp (i.e. page number)
    page = int(res.group(1))
    next_page = 'https://www.pbs.org/newshour/world/page/{}'.format(page + 1)

    return Request(next_page, callback=spider.parse)
