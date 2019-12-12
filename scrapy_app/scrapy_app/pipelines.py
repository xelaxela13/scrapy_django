# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapyitem.models import TestScrapyModel


class ScrapyAppPipeline(object):

    def process_item(self, item, spider):
        domain = item.pop('domain', None)
        url = item.pop('url', None)
        spider_name = item.pop('spider_name', None)
        return TestScrapyModel.objects.update_or_create(domain=domain,
                                                        url=url,
                                                        spider_name=spider_name,
                                                        defaults=item)[0] if domain and url else None


class ScrapyAppCreateOnlyPipeline(object):

    def process_item(self, item, spider):
        return TestScrapyModel.objects.create(**item)
