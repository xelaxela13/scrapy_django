# -*- coding: utf-8 -*-
import json
from scrapy.spiders import Rule
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from .basespider import BaseSpider
from pdb import set_trace


class LinkedInSpider(BaseSpider):
    name = 'linkedinspider'
    allowed_domains = ['linkedin.com']
    login_url = 'https://www.linkedin.com/login'
    start_urls = [
        login_url,
        'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22ua%3A0%22%5D&facetNetwork=%5B%22O%22%5D&keywords=python%20developer&origin=FACETED_SEARCH'
    ]
    custom_settings = {'ROBOTSTXT_OBEY': False}

    def parse(self, response):
        data = {
            'session_key': '',
            'session_password': '',
        }
        yield FormRequest.from_response(response, formdata=data, callback=self.after_login)

    def after_login(self, response):
        yield Request(url=self.start_urls[1], callback=self.parse_item)

    def parse_item(self, response):
        super().parse_item(response)
        # response = Selector(response)
        open_in_browser(response)
        tmp = []
        with open('1.json', 'a') as f:
            for i in response.xpath('//code/text()').getall():
                try:
                    tmp.append(json.loads(i))
                    json.dump(json.loads(i), f)
                except json.decoder.JSONDecodeError:
                    tmp.append(i)
                    json.dump(i, f)

        set_trace()
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
