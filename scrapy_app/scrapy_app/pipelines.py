# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapyitem.models import TestScrapyModel


class ScrapyAppPipeline(object):

    def process_item(self, item, spider):
        return TestScrapyModel.objects.update_or_create(**item)[0]
