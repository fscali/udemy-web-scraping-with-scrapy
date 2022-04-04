import scrapy
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scrapy_selenium import SeleniumRequest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class SlickdealsSpider(scrapy.Spider):
    name = 'slickdeals'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals/',
            # wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):

        driver = response.meta['driver']
        wait = WebDriverWait(driver, 5)

        gdprModal = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@data-template='gdprModal']"))
        )
        if gdprModal:
            button = gdprModal.find_element(By.XPATH, ".//button[1]")
            button.click()

        while True:
            try:
                next_page = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//a[@data-role='next-page']"))
                )
                html = driver.page_source
                sel = Selector(text=html)
                yield from self.get_products(sel, response)

                next_page.click()
                #next_page = wait.until(EC.staleness_of(next_page))
            except NoSuchElementException:
                break
            except TimeoutException:
                break

        driver.close()

    def get_products(self, sel, response):
        cards = sel.xpath("//div[@id='fpMainContent']//div[@class='fpItem  ']")

        # //a[@data-role='next-page']
        for card in cards:
            shop = card.xpath(".//span[@class='blueprint']/a/text()").get()
            url = card.xpath(".//div[@class='itemImageLink']/a/@href").get()
            price = card.xpath(
                ".//div[contains(@class,'itemPrice')]/text()").get()
            price = price.strip() if price else None
            if not shop:
                shop = card.xpath(
                    ".//span[@class='blueprint']/button/text()").get()
            yield {
                'shop': shop,
                'url': response.urljoin(url),
                'price': price
            }
