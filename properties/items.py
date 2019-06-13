# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item ,Field


class PropertiesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # Primary fields
    title = Field()
    price = Field()
    description = Field()
    address = Field()
    image_urls = Field()

    # Calulated fields
    image = Field()
    location = Field()

    # Houskeeping fields
    url = Field()
    project = Field()
    spieder = Field()
    server = Field()
    date = Field()