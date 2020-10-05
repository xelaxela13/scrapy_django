# -*- coding: utf-8 -*-
import json
from .basespider import BaseSpider
from ipdb import set_trace


class Bobry(BaseSpider):
    name = 'bobry'
    allowed_domains = ['bobry.ua']
    start_urls = [
        'https://bobry.ua/calculator',
        'https://bobry.ua/ua/calculator'
    ]

    def process_results(self, response, results):
        return self.parse_item(response, results=results)

    def parse_item(self, response, **kwargs):
        super().parse_item(response)
        self.logger.info('RESPONSE URL: %s', response.url)
        tmp = dict()
        sections = response.xpath('//div[contains(@id, "section")]')
        for section in sections:
            names = [i.strip() for i in section.css('.work::text').extract()]
            values = [i.strip() for i in section.css('.work-row span.hidden-xs::text').extract()]
            tmp[section.xpath('h2/span/text()').get().strip()] = tuple(map(lambda *x: x, names, values))
        filename = 'res_us.json' if response.url == 'https://bobry.ua/ua/calculator' else 'res.json'
        with open(filename, 'w') as f:
            json_data = json.dumps(tmp, ensure_ascii=False)
            f.write(json_data)
        for key, value in tmp.items():
            for name in value:
                self.item['f1'] = key
                self.item['f2'] = name[0]
                self.item['f3'] = name[1]
                yield self.item
