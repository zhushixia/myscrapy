# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re
from pymongo import MongoClient
import hashlib



class MyscrapyPipeline(object):


    def open_spider(self, spider): # 每次爬虫启动时,调用一次.close_spider,爬虫调用结束时调用一次
        client = MongoClient()
        if spider.name == 'sun':
            self.collection = client['sun']['sun']
        if spider.name == 'suning':
            self.collection = client['suning']['suning']
        if spider.name == 'dangdang':
            self.collection = client['dang']['dang']


    def process_item(self, item, spider):
        if spider.name == 'sun':
            item["content"] = self.process_content(item['content'])
            self.collection.insert_one(item)
            return item

        if spider.name == 'suning':
            self.collection.insert_one(item)
            return item

        if spider.name == 'dangdang':
            item['b_cate'] = ''.join([i.strip() for i in item['b_cate']])
            item['m_cate'] = ''.join([i.strip() for i in item['m_cate']])
            item["_id"] = self.add_id(item)
            print(item)
            self.collection.insert_one(item)

    def close_spider(self, spider):
        pass

    def process_content(self, content):
        content = [re.sub("\\xa0|\s", "", i) for i in content]
        content = [i for i in content if len(i)>0]
        return content

    def add_id(self, item):
        sha1 = hashlib.sha1()
        sha1.update(json.dumps(item).encode('utf8'))
        return sha1.hexdigest()
