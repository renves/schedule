from scrapy.crawler import CrawlerProcess
from main import ScrapSpider
import ipdb
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ScrapSpider)
    ipdb.set_trace()
    process.start()
    ipdb.set_trace()