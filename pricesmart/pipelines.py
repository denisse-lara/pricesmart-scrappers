# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import json

from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter


class ExportPipeline:
    def open_spider(self, spider):
        self.logger = logging.getLogger()
        self.file = open(f"{spider.name}.jl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if not item:
            raise DropItem(f"Skipping invalid item")

        adapter = ItemAdapter(item)

        self.logger.info(f"EXPORTING: {str(adapter.get('name'))}")
        line = json.dumps(adapter.asdict()) + "\n"
        self.file.write(line)
        return item
