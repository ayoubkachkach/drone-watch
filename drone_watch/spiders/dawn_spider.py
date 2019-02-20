import scrapy

class DawnSpider(scrapy.Spider):
    name = 'dawn'

    date_str = datetime.datetime.today().strftime('%Y-%m-%d')

    start_urls = [
        'https://www.dawn.com/newspaper/front-page/',
        'https://www.dawn.com/newspaper/back-page/',
        'https://www.dawn.com/newspaper/national/',
        'https://www.dawn.com/newspaper/international/',
        'https://www.dawn.com/newspaper/lahore/',
        'https://www.dawn.com/newspaper/islamabad/',
        'https://www.dawn.com/newspaper/peshawar/',
        'https://www.dawn.com/newspaper/karachi'
    ]

     def parse(self, response):
        page = response.url.split("/")[-2]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)