# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#class App522Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    pass

class App522AppItem(scrapy.Item):
    appname=scrapy.Field()
    downloadcount=scrapy.Field()
    size=scrapy.Field()
    updated=scrapy.Field()
    type=scrapy.Field()
    tag=scrapy.Field()
    

class App522InfoItem(scrapy.Item):
    title=scrapy.Field()
    content=scrapy.Field()
