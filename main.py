import datetime
import pendulum
import os
import scrapy
from scrapy.http import Request
import gspread
import pandas as pd

name = 'ScrapSpider'
dir_path = os.path.dirname(os.path.realpath(__file__))

gc = gspread.service_account(
    filename='credentials.json')
sh = gc.open_by_key('1mi3k6fMBidr2uBLnOcgJoptPdml1j6_EQLJGItbeFkk')
worksheet_list = sh.worksheets()

wk_us = sh.worksheet("US")
wk_uk = sh.worksheet("UK")
LIST = []
LIST_US = []
LIST_UK = []


class ScrapSpider(scrapy.Spider):
    name = 'scrap'
    cont = 0
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }
    def start_requests(self):
        urls = [
            'https://uk.tradingview.com/markets/stocks-united-kingdom/market-movers-gainers/',
            'https://uk.tradingview.com/markets/stocks-united-kingdom/market-movers-losers/',
            'https://uk.tradingview.com/markets/stocks-usa/market-movers-gainers/',
            'https://uk.tradingview.com/markets/stocks-usa/market-movers-losers/']
        for url in urls:
            yield Request(url=url, dont_filter=False)

    def parse(self, response):
        global LIST_US
        global LIST_UK
        global LIST
        self.cont += 1
        now_us = datetime.date.strftime(pendulum.now(
            "US/Eastern"), '%Y-%m-%d %H:%M:%S %Z%z')
        now_uk = datetime.date.strftime(pendulum.now(
            "UTC"), '%Y-%m-%d %H:%M:%S %Z%z')

        stock_market = response.css(
        "#js-category-content > header > div > div.tv-category-header__title-line > div > span > span > h1::text").extract_first().split()[0]

        if stock_market == 'US':
            date_time = now_us
        elif stock_market == 'UK':
            date_time = now_uk

        
        tickers_codes = response.css(
            ".tv-screener__symbol::text").extract()

        tickers_names = response.css(
            ".tv-screener__description::text").extract()

        prices = response.css(
            "#js-screener-container > div.tv-screener__content-pane > table > tbody > tr > td:nth-child(2)::text").extract()

        percentual_changes = response.css(
            "#js-screener-container > div.tv-screener__content-pane > table > tbody > tr > td:nth-child(3)::text").extract()

        absolute_changes = response.css(
            "#js-screener-container > div.tv-screener__content-pane > table > tbody > tr > td:nth-child(4)::text").extract()

        for ticker_code, ticker_name, price, percentual_change, absolute_change in zip(tickers_codes, tickers_names, prices, percentual_changes, absolute_changes):
            
            LIST.append([date_time, stock_market, ticker_code, ticker_name.strip(), float(price), float(
                percentual_change.replace("%", '')), float(absolute_change)])

        df = pd.DataFrame(LIST)
        df = df.drop_duplicates(subset=[2]).sort_values(by=[5])
        df_us = df[df[1]=='US']
        df_uk = df[df[1]=='UK']
        LIST_US = df_us.values.tolist()
        LIST_UK = df_uk.values.tolist()

        if self.cont == 4:  
            if stock_market == 'US':
                wk_us.append_rows(LIST_US) 
                print('US append')
            elif stock_market == 'UK':
                wk_uk.append_rows(LIST_UK)
                print('UK append')
