# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from w3lib.html import remove_tags
import re
from scrapy.selector import Selector


def parse_anchor(a):
    s = Selector(text=a)
    link = s.xpath('//a/@href').get()
    name = ' '.join(s.xpath('//a/text()').getall())

    return dict(url=link, name=name)


class PracticeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LegaBasketItem(scrapy.Item):
    team1 = scrapy.Field()
    team2 = scrapy.Field()
    score = scrapy.Field()


class DigitaliaItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    links = scrapy.Field()
    gingilli = scrapy.Field()


class DigitaliaItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = TakeFirst()

    authors_in = MapCompose(parse_anchor)
    links_in = MapCompose(parse_anchor)
    gingilli_in = MapCompose(parse_anchor)

    authors_out = Identity()
    links_out = Identity()
    gingilli_out = Identity()


class LegaBasketItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.upper, str.strip)

    score_out = Join(separator=' - ')
