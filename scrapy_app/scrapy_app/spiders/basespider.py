# -*- coding: utf-8 -*-
import scrapy


class BasespiderSpider(scrapy.Spider):
    name = 'basespider'
    allowed_domains = ['www.wxample.com']
    start_urls = ['http://www.wxample.com/']

    def parse(self, response):
        pass
