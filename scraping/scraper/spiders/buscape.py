import scrapy
from scrapy.http import Request
from urllib.parse import urljoin


class BuscapeSpider(scrapy.Spider):
    name = 'buscape'
    allowed_domains = ['www.buscape.com.br']
    start_urls = ['https://www.buscape.com.br/']

    _title_selector = '//div[contains(@class, "card--product__name")]/text()'

    def __init__(self, n_pages=20, product_url_suffix=''):
        self.n_pages = int(n_pages)
        self.product_url_suffix = product_url_suffix

    def parse(self, response):
        base_url = urljoin(response.url, self.product_url_suffix)

        for i in range(0, self.n_pages):
            yield Request(
                f'{base_url}?pagina={i + 1}',
                callback=self.parse_page
            )

    def parse_page(self, response):
        titles = response.xpath(self._title_selector).extract()
        return {'titles': titles}