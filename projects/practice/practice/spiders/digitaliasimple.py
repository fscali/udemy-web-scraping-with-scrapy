import scrapy


class DigitaliasimpleSpider(scrapy.Spider):
    name = 'digitaliasimple'
    allowed_domains = ['digitalia.fm']
    start_urls = ['https://digitalia.fm/']

    def parse(self, response):
        title = response.xpath('//h2/a/text()').get()
        yield {
            "title": title
        }
        next_page = response.xpath('//li[@class="prev"]/a')
        for a in next_page:
            yield response.follow(a, callback=self.parse)
