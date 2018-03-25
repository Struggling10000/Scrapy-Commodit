# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapycommoditItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    itemId = scrapy.Field()
    itemTitle = scrapy.Field()
    itemPrice = scrapy.Field()
    itemImg = scrapy.Field()
    #itemDesc = scrapy.Field()
