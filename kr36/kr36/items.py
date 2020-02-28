# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Kr36Item(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    article_id = scrapy.Field()
    _id = scrapy.Field()
    title = scrapy.Field()
    introduction = scrapy.Field()
    time = scrapy.Field()
    introduction_img = scrapy.Field()
    user_name = scrapy.Field()
    user_img = scrapy.Field()
    article_class = scrapy.Field()
    content = scrapy.Field()
