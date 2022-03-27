import scrapy
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
        img = response.meta['screenshot']
        with open('screenshot.png', 'wb') as f:
            f.write(img)


# search_form_input_homepage
# search_button_homepage
