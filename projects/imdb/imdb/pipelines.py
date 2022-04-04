# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo


class MongodbPipeline:
    collection_name = "best_movies"

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        logging.warning(self.mongo_uri)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get("MONGO_URI"))

    def open_spider(self, spider):
        logging.warning("SPIDER OPENED FROM PIPELINE")
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        self.client.close()
        logging.warning("SPIDER CLOSED FROM PIPELINE")

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item
