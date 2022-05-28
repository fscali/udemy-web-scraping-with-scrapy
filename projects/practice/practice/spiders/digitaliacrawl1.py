import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Digitaliacrawl1Spider(CrawlSpider):
    name = 'digitaliacrawl1'
    allowed_domains = ['digitalia.fm']
    start_urls = ['https://digitalia.fm/']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//li[@class="prev"]'), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response):
        title = response.xpath('//h2/a/text()').get()
        yield {
            "title": title
        }

    def parse_item(self, response):
        title = response.xpath('//h2/a/text()').get()
        yield {
            "title": title
        }
