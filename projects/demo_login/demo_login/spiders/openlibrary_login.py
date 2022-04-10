import scrapy


class OpenlibraryLoginSpider(scrapy.Spider):
    name = 'openlibrary_login'
    allowed_domains = ['openlibrary.org']
    start_urls = ['http://openlibrary.org/account/login']

    username = '...'
    password = '...'

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formid='register',
            # formxpath='//form[@id="register"]',
            formdata={
                'username': self.username,
                'password': self.password,
                'redirect': response.xpath('//input[@id="redirect"]/@value').get(),
                'login': 'Log In',
                'debug_token': response.xpath('//input[@id="debug_token"]/@value').get()
            },
            callback=self.after_login

        )

    def after_login(self, response):
        nickname = response.xpath(
            "//div[contains(@class,'account-settings-menu')]/a/text()").get()
        print(nickname)
