# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from pymongo import MongoClient



class MyscrapyPipeline(object):

    def open_spider(self, spider): # 每次爬虫启动时,调用一次.close_spider,爬虫调用结束时调用一次
        client = MongoClient()
        if spider.name == 'sun':
            self.collection = client['sun']['sun']
        if spider.name == 'suning':
            self.collection = client['suning']['suning']


    def process_item(self, item, spider):
        if spider.name == 'sun':
            item["content"] = self.process_content(item['content'])
            self.collection.insert_one(item)
            print(item)
            return item

        if spider.name == 'suning':
            self.collection.insert_one(item)
            print(item)
            return item

    def process_content(self, content):
        content = [re.sub("\\xa0|\s", "", i) for i in content]
        content = [i for i in content if len(i)>0]
        return content
