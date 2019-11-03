# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ScrapyAppItem


class BasespiderSpider(CrawlSpider):
    name = 'basespider'
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
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = ScrapyAppItem()
        first_name = response.xpath('//meta[@itemprop="givenName"]/@content').get()
        last_name = response.xpath('//meta[@itemprop="familyName"]/@content').get()
        city = response.xpath('//meta[@itemprop="addressLocality"]/@content').get()
        phone = response.css('a.profile-view-popup__phone::text').extract_first()
        if first_name and last_name and city and phone:
            item['name'] = first_name + ' ' + last_name if first_name and last_name else None
            item['city'] = city
            item['phone'] = phone
            yield item
