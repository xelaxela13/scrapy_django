# -*- coding: utf-8 -*-
import json
from .basespider import BaseSpider


class LinkedInSpider(BaseSpider):
    name = 'bobry'
    allowed_domains = ['bobry.ua']
    start_urls = [
        'https://bobry.ua/calculator'
    ]

    def parse(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        super().parse_item(response)
        self.logger.info('RESPONSE URL: %s', response.url)
        tmp = dict()
        sections = response.xpath('//div[contains(@id, "section")]')
        for section in sections:
            tmp[section.xpath('h2/span/text()').get().strip()] = [i.strip() for i in
                                                                  section.css('.work::text').extract()]
        with open('res.json', 'w') as f:
            json_data = json.dumps(tmp, ensure_ascii=False)
            f.write(json_data)
        for key, value in tmp.items():
            for name in value:
                self.item['f1'] = key
                self.item['f2'] = name
                yield self.item
