import scrapy
from urllib.parse import urljoin
from books_to_scrape_with_medias.items import BooksToScrapeWithMediasItem


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        articles = response.xpath('//article')
        for article in articles:
            title = article.xpath('./h3/a/text()').get()
            img_url = article.xpath('.//img/@src').get()
            img_url = urljoin(response.url, img_url)
            yield {
                'title': title,
                'image_urls': [img_url]
            }
        next_ = response.xpath(
            "//li[@class='next']/a/@href").get()
        if next_:
            next_ = urljoin(response.url, next_)
            yield scrapy.Request(url=next_, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            })
