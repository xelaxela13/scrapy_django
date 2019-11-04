# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from .basespider import BaseSpider


class TestSpider(BaseSpider):
    name = 'testspider'
    allowed_domains = ['mywed.com']
    start_urls = [
        'https://mywed.com/ru/Ukraine-wedding-photographers/',
    ]

    rules = (
        Rule(LinkExtractor(allow=(r'\/ru\/photographer\/\w+\/$',
                                  r'\/ru\/Ukraine-wedding-photographers\/p\d+'
                                  )
                           ),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        super().parse_item(response)
        self.logger.info('RESPONSE URL: %s', response.url)
        first_name = response.xpath('//meta[@itemprop="givenName"]/@content').get()
        last_name = response.xpath('//meta[@itemprop="familyName"]/@content').get()
        site = response.xpath('//a[@itemprop="sameAs"]/@href').get()
        city = response.xpath('//meta[@itemprop="addressLocality"]/@content').get()
        phone = response.css('a.profile-view-popup__phone::text').extract_first()
        if first_name and last_name and city and phone:
            self.item['name'] = first_name + ' ' + last_name if first_name and last_name else None
            self.item['city'] = city
            self.item['site'] = site
            self.item['phone'] = phone
            yield self.item
