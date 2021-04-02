from datetime import datetime
import os
import scrapy
from scrapy.http import Request
import gspread
import ipdb

name = 'ScrapSpider'
dir_path = os.path.dirname(os.path.realpath(__file__))

gc = gspread.service_account(
    filename='credentials.json')
sh = gc.open_by_key('1mi3k6fMBidr2uBLnOcgJoptPdml1j6_EQLJGItbeFkk')
worksheet_list = sh.worksheets()

wk_us = sh.worksheet("US")
wk_uk = sh.worksheet("UK")


class ScrapSpider(scrapy.Spider):
    name = 'scrap'
    def start_requests(self):
        urls = [
            'https://uk.tradingview.com/markets/stocks-united-kingdom/market-movers-gainers/']
        for url in urls:
            yield Request(url=url, dont_filter=False)

    def parse(self, response):
        text = response.css(
            ".tv-breadcrumbs__item:nth-child(2)::text").extract_first()
        wk_us.append_row([text])
