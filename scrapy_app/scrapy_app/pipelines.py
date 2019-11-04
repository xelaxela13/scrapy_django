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
        return TestScrapyModel.objects.update_or_create(domain=domain,
                                                        url=url,
                                                        defaults=item)[0] if domain and url else None
