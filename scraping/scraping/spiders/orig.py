# import scrapy
# from selenium import webdriver

# class ArchiveSpider(Spider):
#     name = 'archive'
#     start_urls = []

#     # custom_settings = {
#     #     'LOG_FILE': 'archive.log',
#     # }

#     def __init__(self, website_str=''):
#         self.website = websites.get(website_str.upper(), None)
#         self.page_number = 1
#         if (self.website is None):
#             raise ValueError(
#                 'No website {} available. Enter one of the following websites: {}'
#                 .format(website_str, list(websites.keys())))

#         self.next_request = self.website.next_request
#         self.rules = [
#             Rule(
#                 LinkExtractor(allow=self.website.url_patterns),
#                 callback=self.parse_article)
#         ]
#         self.start_urls = self.website.seed_urls
#         self.source = Source.objects.get_or_create(
#             name=self.website.name,
#             homepage=self.website.homepage,
#             favicon=self.website.favicon)[0]

#     def parse(self, response):
#         website = self.website
#         # extract all links from current page that respect pattern
#         links = set(response.css('a::attr(href)').re(website.url_patterns))
#         if (not links):
#             self.logger.info('No link found. Stopping scraper.')
#             return

#         # if website uses relative url, prepend all links with domain name
#         if (website.relative_url):
#             links = (response.urljoin(link) for link in links if link)

#         # only keep unvisited links
#         links = (link for link in links if not Article.objects.filter(url=link))

#         for link in links:
#             yield response.follow(link, callback=self.parse_article)

#         request = self.next_request(self, response)
#         # if there is no next page, stop
#         if (not request):
#             return

#         self.page_number +=1
#         yield request

#     def parse_article(self, response):
#         website = self.website
#         title = ''
#         body = ''
#         date = None

#         titles = response.xpath(
#             '//*[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
#             website.title_class).getall()
#         if (not titles):
#             self.logger.warning('No title found for article in {}'.format(
#                 response.url))
#         else:
#             title = titles[0].strip()

#         # append text from all children nodes into one
#         paragraphs = response.xpath(
#             '//div[contains(@class, \'%s\')]/descendant-or-self::*/text()' %
#             website.body_class).getall()
#         if (paragraphs):
#             body = '\n'.join(p.strip() for p in paragraphs)
#         else:
#             self.logger.warning('No body found for article in {}'.format(
#                 response.url))
#             return

#         # append text from all children nodes into one
#         dates = response.xpath('//*[contains(@class, \'%s\')]/text()' %
#                                website.date_class).getall()

#         date = parse_date(dates)

#         if (not date):
#             self.logger.warning('No date found for article in {}'.format(
#                 response.url))

#         # clean body from javascript escape characters
#         body = re.sub(re.compile('\\xad'), '', body)
#         body = re.sub(re.compile('\\n'), ' ', body)

#         article_item = ArticleItem(
#             title=title,
#             body=body,
#             date_published=date,
#             url=response.url,
#             source=self.source)

#         yield article_item
