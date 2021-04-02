
from scrapy.crawler import CrawlerProcess

from apscheduler.schedulers.twisted import TwistedScheduler

from main import ScrapSpider

process = CrawlerProcess()
scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'interval', args=[ScrapSpider], seconds=5)
scheduler.start()
process.start(False)