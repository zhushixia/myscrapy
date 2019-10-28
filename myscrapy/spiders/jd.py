# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['book.jd.com']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')
        for dt in dt_list:
            item = {}
            item['b_cate'] = dt.xpath('./a/text()').extract_first()
            em_list = dt.xpath('./following-sibling::*[1]/em')
            for em in em_list:
                item['m_cate'] = em.xpath('./a/text()').extract_first()
                item['m_href'] = 'https:'+em.xpath('./a/@href').extract_first()
                yield scrapy.Request(item['m_href'], callback=self.parse_detail, meta={'item': deepcopy(item)})

    def parse_detail(self, response):
        item = response.meta.get('item')

