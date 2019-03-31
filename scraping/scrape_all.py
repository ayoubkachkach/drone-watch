from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
spider = 'archive'
# 'followall' is the name of one of the spiders of the project.
for website in ['pbs', 'reuters', 'dawn']:
    process.crawl(spider, website_str=website)
process.start()
