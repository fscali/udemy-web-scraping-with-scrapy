import scrapy


class GlassesshopSpider(scrapy.Spider):
    name = 'glassesshop'
    allowed_domains = ['www.glassesshop.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        })

    def parse(self, response):
        products = response.xpath(
            "//div[contains(@class, 'product-list-item')]")
        for product in products:
            name = product.xpath(
                "(.//a[contains(@class,'product-title')])[position()=1]/text()").get()
            price = product.xpath(
                ".//div[@class='p-price']/div/span/text()"
            ).get()
            url = product.xpath(".//div[@class='p-title']/a/@href").get()
            image_url = product.xpath(
                ".//img[@class='lazy d-block w-100 product-img-default']/@src").get()

            yield {
                'name': name.strip(),
                'price': price,
                'url': url,
                'image_url': image_url
            }

        next = response.xpath(
            "//ul[@class='pagination']/li[position()=last()]/a/@href").get()
        if next:
            yield scrapy.Request(url=next, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            })
