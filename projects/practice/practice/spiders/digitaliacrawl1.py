from logging import FileHandler
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.logformatter import LogFormatter
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from practice.items import DigitaliaItem, DigitaliaItemLoader


class Digitaliacrawl1Spider(CrawlSpider):
    name = 'digitaliacrawl1'
    allowed_domains = ['digitalia.fm']
    start_urls = ['https://digitalia.fm/']

    def __init__(self, *a, **kw):
        self.logger.setLevel('DEBUG')
        handler = FileHandler('/tmp/digitaliaspider.log')

        #handler.format = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
        self.logger.logger.addHandler(handler)
        super().__init__(*a, **kw)

    def errback_handler(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    def parse_start_url(self, response):
        yield from self.parse_item(response)

    def parse_item(self, response):

        self.logger.info(
            'Got successful response from {}'.format(response.url))
        l = DigitaliaItemLoader(item=DigitaliaItem(), response=response)
        l.add_xpath("title", '//h2/a/text()')
        l.add_xpath("url", '//h2/a/@href')
        l.add_xpath("authors", '//ul[contains(@class, "speaker")]/li/a')

        l.add_xpath("gingilli", '//section[@id="article-gingilli"]//a')
        l.add_xpath("links", '//section[@id="article-link"]//a')
        yield l.load_item()

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//li[@class="prev"]'), callback='parse_item', follow=True, errback=errback_handler),
    )
