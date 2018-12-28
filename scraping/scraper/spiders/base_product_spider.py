import scrapy
from scrapy.http import Request

from .product import ProductList

class BaseProductSpider(scrapy.Spider):
    allowed_domains = ['www.buscape.com.br']
    start_urls = ['https://www.buscape.com.br/']

    _title_selector = '//div[contains(@class, "card--product__name")]/text()'
    _next_page_url_selector = '//li[contains(@class, "pagination__item")]/a[i]/@href'

    def parse(self, response):
        base_url = f'{response.url}/{self.product_url_suffix}'

        for i in range(0, self.n_pages):
            yield Request(
                f'{base_url}?pagina={i + 1}',
                callback=self.parse_page
            )

    def parse_page(self, response):
        titles = response.xpath(self._title_selector).extract()
        product_list = ProductList()
        product_list['titles'] = titles
        return product_list