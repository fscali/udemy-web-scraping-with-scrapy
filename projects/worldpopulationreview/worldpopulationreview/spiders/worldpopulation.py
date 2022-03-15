import scrapy


class WorldpopulationSpider(scrapy.Spider):
    name = 'worldpopulation'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = [
        'https://worldpopulationreview.com/countries/countries-by-national-debt']

    def parse(self, response):
        countries = response.xpath("//tbody/tr")
        for country in countries:
            name = country.xpath(".//td[1]/a/text()").get()
            ratio = country.xpath(".//td[2]/text()").get()
            population = country.xpath(".//td[3]/text()").get()
            yield {
                'country': name,
                'ratio': ratio,
                'population': population

            }

            # absolute_url = f'https://www.worldometers.info/{link}'
            # absolute_url = response.urljoin(link)
            # yield response.follow(url=link, callback=self.parse_country, meta={'country': name})

    """  def parse_country(self, response):
        name = response.request.meta.get('country')
        rows = response.xpath(
            "(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")

        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                'country': name,
                'year': year,
                'population': population
            } """
