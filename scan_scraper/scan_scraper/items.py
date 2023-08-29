# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScanProductItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    SKU = scrapy.Field()
    link = scrapy.Field()

class ScanGpuItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    SKU = scrapy.Field()
    link = scrapy.Field()
    availability = scrapy.Field()
    dimensions = scrapy.Field()
    model_number = scrapy.Field()
    chipset = scrapy.Field()
