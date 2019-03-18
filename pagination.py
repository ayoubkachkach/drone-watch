from datetime import datetime, timedelta
import re


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
    return 'https://www.pbs.org/newshour/world/page/{}'.format(page + 1)