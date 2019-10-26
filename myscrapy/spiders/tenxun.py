# -*- coding: utf-8 -*-
import json

import scrapy


class TenxunSpider(scrapy.Spider):
    name = 'tenxun'
    allowed_domains = ['careers.tencent.com']
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1571839266759&countryId=&cityId=&bgIds=&productId=&categoryId=40001001,40001002,40001003,40001004,40001005,40001006,40003001,40003002,40003003,40002001,40002002,40004,40005001,40005002,40006,40007,40008,40009,40010,40011&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn']

    def parse(self, response):
        ret = json.loads(response.text)
        posts = ret.get('Data').get('Posts')
        for i in posts:
            item = {}
            item['CountryName'] = i.get('CountryName')
            item['RecruitPostName'] = i.get('RecruitPostName')
            item['CategoryName'] = i.get('CategoryName')
            item['Responsibility'] = i.get('Responsibility')
            item['PostURL'] = i.get('PostURL')
            item['LastUpdateTime'] = i.get('LastUpdateTime')
            print(item)
            yield item
        # 构造下一个url
        for i in range(2,500):
            next_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1571839266759&countryId=&cityId=&bgIds=&productId=&categoryId=40001001,40001002,40001003,40001004,40001005,40001006,40003001,40003002,40003003,40002001,40002002,40004,40005001,40005002,40006,40007,40008,40009,40010,40011&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'.format(i)
            yield scrapy.Request(next_url, callback=self.parse)
