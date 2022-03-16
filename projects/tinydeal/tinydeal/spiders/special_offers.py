import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com']
    # start_urls = [
    #    'https://www.cigabuy.com/builtin-battery-c-56_139.html']

    def start_requests(self):
        yield scrapy.Request(url='https://www.cigabuy.com/builtin-battery-c-56_139.html', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        })

    def parse(self, response):
        product_boxes = response.xpath("//*[@class='p_box_wrapper']")
        for box in product_boxes:
            title = box.xpath(".//a[@class='p_box_title']/text()").get()
            discounted_price = box.xpath(
                ".//span[@class='productSpecialPrice fl']/text()").get()
            normal_price = box.xpath(
                ".//span[@class='normalprice fl']/text()").get()
            if not normal_price:
                normal_price = box.xpath(
                    ".//div[@class='p_box_price cf']/text()").get()
            url = box.xpath(".//a[@class='p_box_title']/@href").get()
            yield {
                'title': title,
                'normal_price': normal_price,
                'discounted_price': discounted_price,
                'url': url,
                'User-Agent': response.request.headers['User-Agent']
            }
        next_page = response.xpath(
            "(//a[@class='nextPage'])[position()=1]/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            })
