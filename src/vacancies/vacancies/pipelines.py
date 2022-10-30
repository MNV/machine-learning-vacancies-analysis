# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
# useful for handling different item types with a single interface

import sys

import pymongo
from pymongo.database import Database
from scrapy import Item, Spider
from scrapy.crawler import Crawler

from vacancies.items import VacancyItem


class MongoDBPipeline:
    """
    Сохранение информации в базе данных MongoDB.
    """

    # название коллекции в БД MongoDB
    collection = "vacancies"

    def __init__(self, mongodb_uri: str, mongodb_db: str) -> None:
        self.mongodb_uri = os.getenv("MONGODB_URI", mongodb_uri)
        self.mongodb_db = os.getenv("MONGODB_DATABASE", mongodb_db)
        if not self.mongodb_uri:
            sys.exit("You need to provide a Connection String.")

        self.client: pymongo.MongoClient
        self.database: Database

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "MongoDBPipeline":
        return cls(
            mongodb_uri=crawler.settings.get("MONGODB_URI"),
            mongodb_db=crawler.settings.get("MONGODB_DATABASE", "items"),
        )

    def open_spider(self, spider: Spider) -> None:
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.database = self.client[self.mongodb_db]

    def close_spider(self, spider: Spider) -> None:
        self.client.close()

    def process_item(self, item: Item, spider: Spider) -> Item:
        data = dict(VacancyItem(item))
        self.database[self.collection].replace_one(
            {"id": data["id"]}, data, upsert=True
        )

        return item
