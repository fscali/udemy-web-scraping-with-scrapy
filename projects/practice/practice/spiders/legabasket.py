from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from practice.items import LegaBasketItem, LegaBasketItemLoader


class LegabasketSpider(CrawlSpider):
    name = 'legabasket'
    allowed_domains = ['www.legabasket.it']
    start_urls = [
        'https://www.legabasket.it/lba/6/calendario?c=429&d=1&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=2&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=3&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=4&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=5&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=6&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=7&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=8&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=9&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=10&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=11&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=12&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=13&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=14&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=15&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=16&p=1&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=17&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=18&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=19&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=20&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=21&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=22&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=23&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=24&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=25&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=26&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=27&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=28&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=29&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=30&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=31&p=2&s=2021&t=0',
        'https://www.legabasket.it/lba/6/calendario?c=429&d=32&p=2&s=2021&t=0',
    ]

    rules = (Rule(LinkExtractor(
        restrict_css='.result.big-shoulders'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """  team_1 = response.xpath(
            '(//span[@class="team-name"])[position()=1]/a/text()').get().strip()
        team_2 = response.xpath(
            '(//span[@class="team-name"])[position()=2]/a/text()').get().strip()
        score_1 = response.xpath(
            '//span[@id="home-score"]/text()').get().strip()
        score_2 = response.xpath(
            '//span[@id="visitor-score"]/text()').get().strip() """
        l = LegaBasketItemLoader(item=LegaBasketItem(), response=response)
        l.add_xpath(
            'team1', '(//span[@class="team-name"])[position()=1]/a/text()')
        l.add_xpath(
            'team2', '(//span[@class="team-name"])[position()=2]/a/text()')
        l.add_xpath('score', '//span[@id="home-score"]/text()')
        l.add_xpath('score', '//span[@id="visitor-score"]/text()')
        yield l.load_item()

        """  yield {
            "team1": team_1,
            "team2": team_2,
            "score": f'{score_1} - {score_2}'}
 """
