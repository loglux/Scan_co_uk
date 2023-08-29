# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class ProductRelatedPipeline:
    def process_item(self, item, spider):
        # Check if the item is a promotional product or "related" product
        if 'related' in item.get('link', ''):
            # Handle the related product differently
            # For example, you might want to skip it:
            return None
        else:
            # Process regular items
            return item

class ScanScraperPipeline:
    def process_item(self, item, spider):
        return item
