# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SongItem(scrapy.Item):
    # define the fields for your item here like:
    song = scrapy.Field()
    artist = scrapy.Field()
    music = scrapy.Field()
    writer = scrapy.Field()
    visits = scrapy.Field()
    genre = scrapy.Field()
    postedBy = scrapy.Field()
    guitarKey = scrapy.Field()
    lyrics = scrapy.Field()
    pass
