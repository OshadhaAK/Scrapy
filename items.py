# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DeranafmItem(scrapy.Item):
    # define the fields for your item here like:
    song = scrapy.Field()
    mainArtist = scrapy.Field()
    music = scrapy.Field()
    lyrics = scrapy.Field()
    visits = scrapy.Field()
    downloads = scrapy.Field()
    downloadFormats = scrapy.Field()
    videoURI = scrapy.Field()
    url = scrapy.Field()
    pass
