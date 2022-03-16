import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com']
    start_urls = [
        'https://www.cigabuy.com/builtin-battery-c-56_139.html']

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
                'url': url
            }
        next_page = response.xpath(
            "(//a[@class='nextPage'])[position()=1]/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
