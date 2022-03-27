import scrapy
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy_selenium import SeleniumRequest


class ExampleSpider(scrapy.Spider):
    name = 'example'
    #allowed_domains = ['example.com']
    #start_urls = ['http://example.com/']

    def start_requests(self):
        yield SeleniumRequest(
            url='https://duckduckgo.com',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):

        driver = response.meta['driver']
        search_input = driver.find_element(By.XPATH,
                                           '//input[@id="search_form_input_homepage"]')
        search_input.send_keys('Hello World')

        # driver.save_screenshot('after_filling_input.png')
        search_input.send_keys(Keys.ENTER)
        # driver.save_screenshot('enter.png')
        html = driver.page_source
        sel = Selector(text=html)
        links = sel.xpath("//div[@class='result__extras__url']/a")

        for link in links:
            yield {
                'url': link.xpath('./@href').get()
            }
