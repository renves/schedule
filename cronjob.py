
from scrapy.crawler import CrawlerProcess

from apscheduler.schedulers.twisted import TwistedScheduler

from main import ScrapSpider

process = CrawlerProcess()
scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'cron', args=[ScrapSpider], hour=20, minute=30)
#scheduler.add_job(process.crawl, 'interval', args=[ScrapSpider], seconds=60)
scheduler.start()
process.start(False)