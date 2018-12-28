import scrapy
from scrapy.http import Request
from urllib.parse import urljoin


def subselect(subquery):
    def do_subselect(partial_results):
        return partial_results.xpath(subquery)
    return do_subselect


class BuscapeSpider(scrapy.Spider):
    name = 'buscape'
    allowed_domains = ['www.buscape.com.br']
    start_urls = ['https://www.buscape.com.br/']

    _product_title_selector = '//div[contains(@class, "card--product__name")]/text()'
    _product_href_selector = '//div[contains(@class, "card--product__name")]/../@href'

    def __init__(self, n_pages=20, category=''):
        self.n_pages = int(n_pages)
        self.category = category
        self.base_url = None

    def parse(self, response):
        self.base_url = urljoin(response.url, self.category)

        for i in range(0, self.n_pages):
            yield Request(
                f'{self.base_url}?pagina={i + 1}',
                callback=self.parse_page
            )

    def parse_page(self, response):
        titles = response.xpath(self._product_title_selector).extract()
        sources = response.xpath(self._product_href_selector).extract()
        sources = map(
            lambda s: urljoin(self.base_url, s),
            sources
        )
        return (
            {
                'TITLE': title,
                'SOURCE': source,
                'CATEGORY': self.category
            } for title, source in zip(titles, sources))