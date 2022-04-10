import scrapy
from scrapy.exceptions import CloseSpider
import json


class EbookSpider(scrapy.Spider):
    name = 'ebook'
    allowed_domains = ['openlibrary.org']
    step = 100
    start_urls = [
        f'https://openlibrary.org/subjects/picture_books.json?limit=100']

    """  def start_requests(self):
        yield scrapy.Request(url=f'https://openlibrary.org/subjects/picture_books.json?limit={self.step}')
 """

    def parse(self, response, offset=0):
        # if response.status == 500:
        #    raise CloseSpider('Reached last page...')
        resp = json.loads(response.body)
        work_count = resp.get('work_count')

        ebooks = resp.get('works')
        for ebook in ebooks:
            yield {
                'title': ebook.get('title'),
                'subject': ebook.get('subject')
            }
        offset = offset + self.step
        """ yield scrapy.Request(
            url=f'https://openlibrary.org/subjects/picture_books.json?limit={self.step}&offset={offset}',
            callback=self.parse,
            cb_kwargs=dict(offset=offset)
        ) """

        if offset < work_count:
            offset = offset + self.step
            yield scrapy.Request(
                url=f'https://openlibrary.org/subjects/picture_books.json?limit={self.step}&offset={offset}',
                callback=self.parse,
                cb_kwargs=dict(offset=offset)
            )
