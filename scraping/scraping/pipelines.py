# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.utils import timezone


class ArticlePipeline(object):

    def process_item(self, item, spider):
        if(not item):
            return
        
        item['date_scraped'] = timezone.now()
        item.save()
        return item
