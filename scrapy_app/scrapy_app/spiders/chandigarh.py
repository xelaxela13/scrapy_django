# -*- coding: utf-8 -*-
from scrapy import FormRequest
from .basespider import BaseSpider
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser


class ChandigarhSpider(BaseSpider):
    name = 'chandigarh'
    allowed_domains = ['chandigarh.gov.in', '164.100.147.10']
    start_urls = [
        'http://chandigarh.gov.in',
        'http://164.100.147.10/propertydetail/knowyourproperty.aspx',
    ]
    custom_settings = {'ROBOTSTXT_OBEY': False,
                       'ITEM_PIPELINES': {'scrapy_app.pipelines.ScrapyAppCreateOnlyPipeline': 300}}

    def parse(self, response):
        data = {
            'ctl00$MainContent$txtFileNo': '',
            'ctl00$MainContent$txtPlotNo': '2',
            'ctl00$MainContent$txtSectorNo': '',
            'ctl00$MainContent$drpCategory': '0',
            'ctl00$MainContent$btnSearch': 'Search',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUKLTg0NjU0MjY3MA9kFgJmD2QWAgIDD2QWAgIDD2QWAgILDzwrABECARAWABYAFgAMFCsAAGQYAQUjY3RsMDAkTWFpbkNvbnRlbnQkZ3JkUHJvcGVydHlSZWNvcmQPZ2TkHTt6szMUCbhMv+leRdJRnmjLYXSSCDriOfbyLt4ozQ==',
            '__VIEWSTATEGENERATOR': 'DAD87DCE',
            '__EVENTVALIDATION': '/wEdAAxAgpHyyRbSaqqzij848hkmOwwXTCk4NhtbnrwTJLVEiIlflmIS5jfsJkg5Iz6KivTy2ZVrIMVLjYDcYKIbArbcaTTT0uy00de/Bk9zke0Cop5LtAxolj4ErTqz5mi+08j1ewmWikdws6Ni/bWqUfc/nwIzANUZhjDnBb5pMoDAhlRYE9HJWwIHJ80xH2fJaYcJ8ZyH29pplOqaTQWEZSBWn4j8c9nzo0RlxtfBH2PEDrEzndyr7AoHdDlwBdxcPxdq3Mue765BEIOS9Kkid50gJ50oqewJXXqXFBJGssxAWA=='
        }
        yield FormRequest(self.start_urls[1], formdata=data, callback=self.parse_item,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})

    def parse_item(self, response):
        super().parse_item(response)
        # open_in_browser(response)
        self.logger.info('RESPONSE URL: %s', response.url)
        ids = response.xpath('//*[contains(@id, "MainContent_grdPropertyRecord_lblSrNo")]/text()').getall()
        files = response.xpath('//*[contains(@id, "MainContent_grdPropertyRecord_lnkFileNumber")]').getall()
        property_number = response.xpath(
            '//*[contains(@id, "MainContent_grdPropertyRecord_lblPropertyNumber")]').getall()
        sector_number = response.xpath(
            '//*[contains(@id, "MainContent_grdPropertyRecord_lblSectorNumber")]').getall()
        address = response.xpath('//*[contains(@id, "MainContent_grdPropertyRecord_lblAddress")]').getall()
        category = response.xpath('//*[contains(@id, "MainContent_grdPropertyRecord_lblCategory")]').getall()
        for i, id in enumerate(ids):
            self.item['f1'] = id
            self.item['f2'] = Selector(text=files[i]).xpath('//text()').get() or ''
            self.item['f3'] = Selector(text=property_number[i]).xpath('//text()').get() or ''
            self.item['f4'] = Selector(text=sector_number[i]).xpath('//text()').get() or ''
            self.item['f5'] = Selector(text=address[i]).xpath('//text()').get() or ''
            self.item['f6'] = Selector(text=category[i]).xpath('//text()').get() or ''
            yield self.item
