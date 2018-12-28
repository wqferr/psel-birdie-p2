# -*- coding: utf-8 -*-
import scrapy

from .base_product_spider import BaseProductSpider

class BuscapeSmartphonesSpider(BaseProductSpider):
    name = 'buscape_smartphones'
    product_url_suffix = 'celular-e-smartphone'

    n_pages = 20
