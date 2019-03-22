# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem

from web.models import Article
from web.models import Source


class ArticleItem(DjangoItem):
    django_model = Article