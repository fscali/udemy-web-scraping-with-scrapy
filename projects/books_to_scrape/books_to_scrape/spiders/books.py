import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/index.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//article[@class="product_pod"]/h3/a'),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a')),
    )

    def parse_item(self, response):
        item = {
            'title': response.xpath('//h1/text()').get(),
            'price': response.xpath('//p[@class="price_color"]/text()').get(),
        }
        return item
