# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NetworkrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    siteDomain = scrapy.Field()
    #siteName = scrapy.Field()
    levels = scrapy.Field()
    url = scrapy.Field()
    innerPageArray = scrapy.Field()
    outPageArray = scrapy.Field()
