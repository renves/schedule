
from scrapy.crawler import CrawlerProcess
from apscheduler.schedulers.twisted import TwistedScheduler
from us import ScrapSpiderUS
from uk import ScrapSpiderUK

process = CrawlerProcess()
scheduler = TwistedScheduler()

scheduler.add_job(process.crawl, 'cron', args=[ScrapSpiderUK], hour=10, timezone='UTC')
scheduler.add_job(process.crawl, 'cron', args=[ScrapSpiderUK], hour=10)
scheduler.add_job(process.crawl, 'cron', args=[
                  ScrapSpiderUK], hour=12, minute=30)

scheduler.add_job(process.crawl, 'cron', args=[ScrapSpiderUS], hour=11, timezone='EDC')
scheduler.add_job(process.crawl, 'cron', args=[ScrapSpiderUS], hour=14)
scheduler.add_job(process.crawl, 'cron', args=[
                  ScrapSpiderUS], hour=16, minute=30)

scheduler.start()
process.start(False)
