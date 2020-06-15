# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    typer = scrapy.Field()
    name = scrapy.Field()
    avgScore = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    openTime = scrapy.Field()
    # print(typer)
    # print(name, avgScore)
    # print(address, phone)
    # print(openTime)
