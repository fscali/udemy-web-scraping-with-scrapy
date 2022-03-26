import scrapy
from scrapy.shell import inspect_response
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from shutil import which

import time


class BinanceSpider(scrapy.Spider):
    name = 'binance'
    allowed_domains = ['www.binance.com']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    html = []

    #start_urls = ['https://www.binance.com/en/markets']

    def start_requests(self):
        yield scrapy.Request(url='https://www.binance.com/en/markets', headers={
            'User-Agent': self.user_agent
        })

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--headless")

        chrome_path = "./chromedriver"
        driver = webdriver.Chrome(
            executable_path=chrome_path, options=chrome_options
        )
        driver.get('https://www.binance.com/en/markets')
        # (//header/div[position()=last()]//div[@data-bn-type='text'])[position()=last()]
        cookie_accept = driver.find_element(
            By.ID, "onetrust-accept-btn-handler")
        cookie_accept.click()
        # currency_link = driver.find_element(
        #    By.XPATH, "(//header/div[position()=last()]//div[@data-bn-type='text'])[position()=last()]")
        # currency_link.click()
#        time.sleep(5)
        self.html.append(driver.page_source)
        next_link = True
        while next_link:
            try:
                next_link = driver.find_element(
                    By.XPATH, '(//button[@aria-label="Next page"])[not(@disabled)]')
                if next_link:
                    next_link.click()
                self.html.append(driver.page_source)
            except:
                break
        driver.close()

    def parse(self, response):
        for html in self.html:
            resp = Selector(text=html)

            yield from self.get_page_data(resp)

    def get_page_data(self, selector):
        row_selector = "//div[@class='css-vlibs4']"
        short_name_selector = "./div/div[position()=1]/div[position()=2]/div/text()"
        full_name_selector = "./div/div[position()=1]/div[position()=3]/div/text()"
        price_selector = "./div/div[position()=2]/div/text()"
        rows = selector.xpath(row_selector)
        print(f' length of rows is f{len(rows)}')
        for row in rows:
            yield {
                'short_name': row.xpath(short_name_selector).get(),
                'full_name': row.xpath(full_name_selector).get(),
                'price': row.xpath(price_selector).get(),
            }
