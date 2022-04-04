import scrapy
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        #Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(
            restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_start_url(self, response, **kwargs):
       # inspect_response(response, self)
       # open_in_browser(response)
        return super().parse_start_url(response, **kwargs)

    def parse_item(self, response):
        title = response.xpath("//h1/text()").get()
        year = response.xpath(
            '(//ul[@data-testid="hero-title-block__metadata"])/li[1]/a/text()').get()
        rating = response.xpath(
            '(//div[@data-testid="hero-rating-bar__aggregate-rating__score"])[1]/span[1]/text()').get()
        duration = response.xpath(
            'normalize-space((//ul[@data-testid="hero-title-block__metadata"])/li[3]/text())').get()
        genre = response.xpath(
            '(//div[@data-testid="genres"])//span/text()').get()
        item = {}
        item['title'] = title
        item['year'] = year
        item['duration'] = duration
        item['genre'] = genre
        item['rating'] = rating
        item['movie_url'] = response.url
        #item['user-agent'] = response.request.headers['User-Agent']

        return item
