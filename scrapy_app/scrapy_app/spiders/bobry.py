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
        tmp2 = dict()
        sections = response.xpath('//div[contains(@id, "section")]')
        sub = None
        items = []
        for i, section in enumerate(sections):
            names = [i.strip() for i in section.css('.work::text').extract()]
            values = [i.strip() for i in section.css('.work-row span.hidden-xs::text').extract()]
            tmp[section.xpath('h2/span/text()').get().strip()] = tuple(map(lambda *x: x, names, values))

            for tag in section.xpath('*'):
                if tag.xpath('name()').get() == 'h2':
                    tmp2[i] = {'main': tag.xpath('span/text()').get()}
                if tag.xpath('name()').get() == 'h3':
                    if not sub:
                        sub = tag.xpath('span/text()').get()
                        tmp2[i].update({'sub': {sub: []}})
                    else:
                        tmp2[i]['sub'][sub] = items
                        sub = tag.xpath('span/text()').get()
                        tmp2[i]['sub'].update({sub: []})
                        items = []
                if tag.xpath('name()').get() == 'div':
                    item = [i.strip() for i in tag.css('.work::text').extract()]
                    unit = [i.strip() for i in tag.css('.work-row span.hidden-xs::text').extract()]
                    item.extend(unit)
                    items.append(item)
            if sub:
                try:
                    tmp2[i]['sub'][sub] = items
                except KeyError:
                    tmp2[i]['sub'].update({sub: items})
                sub = None
                items = []
        filename = 'res_ua.json' if response.url == 'https://bobry.ua/ua/calculator' else 'res.json'
        with open(filename, 'w') as f:
            json_data = json.dumps(tmp2, ensure_ascii=False)
            f.write(json_data)
        # for key, value in tmp.items():
        #     for name in value:
        #         self.item['f1'] = key
        #         self.item['f2'] = name[0]
        #         self.item['f3'] = name[1]
        #         yield self.item
        yield
