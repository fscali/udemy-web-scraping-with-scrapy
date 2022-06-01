import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from practice.items import DigitaliaItem, DigitaliaItemLoader


class Digitaliacrawl1Spider(CrawlSpider):
    name = 'digitaliacrawl1'
    allowed_domains = ['digitalia.fm']
    start_urls = ['https://digitalia.fm/']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//li[@class="prev"]'), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response):
        yield from self.parse_item(response)

    def parse_item(self, response):
        l = DigitaliaItemLoader(item=DigitaliaItem(), response=response)
        l.add_xpath("title", '//h2/a/text()')
        l.add_xpath("url", '//h2/a/@href')
        l.add_xpath("authors", '//ul[contains(@class, "speaker")]/li/a')

        l.add_xpath("gingilli", '//section[@id="article-gingilli"]//a')
        l.add_xpath("links", '//section[@id="article-link"]//a')
        yield l.load_item()
