# -*- coding: utf-8 -*-
import scrapy


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']  # 允许爬取的范围
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']  # 爬虫最开始的网址

    def parse(self, response):
        li_list = response.xpath('//div[@class="tea_con"]/div/ul/li')
        for li in li_list:
            item = {}
            item['name'] = li.xpath('.//h3/text()').extract_first()
            item['level'] = li.xpath('.//h4/text()').extract_first()
            item['info'] = li.xpath('.//p/text()').extract_first()
            yield item

