# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider


class BaseSpider(CrawlSpider):
    name = 'basespider'
    allowed_domains = ['example.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = {}

    def parse_item(self, response):
        self.item = {'url': response.url, 'domain': self.allowed_domains[0], 'spider_name': self.name}
