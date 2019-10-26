# -*- coding: utf-8 -*-
import re

import scrapy
from copy import deepcopy


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 获取大分类
        div_list = response.xpath('//div[@class="menu-list"]/div[@class="menu-item"]')
        div_sub_list = response.xpath('//div[@class="menu-list"]/div[@class="menu-sub"]')
        for div in div_list[:1]:
            item = {}
            item['b_cate'] = div.xpath('.//h3/a/text()').extract_first()
            # 当前大分类下的中间分类位置
            current_sub_div = div_sub_list[div_list.index(div)]
            p_list = current_sub_div.xpath('./div[@class="submenu-left"]/p[@class="submenu-item"]')
            for p in p_list[0:1]:
                # 获取中间分类
                item['m_cate'] = p.xpath('./a/text()').extract_first()
                # 获取小分类
                li_list = p.xpath('./following-sibling::ul/li')
                for li in li_list[0:1]:
                    item['s_cate'] = li.xpath('./a/text()').extract_first()
                    item['s_href'] = li.xpath('./a/@href').extract_first()
                    yield scrapy.Request(item['s_href'], callback=self.parse_list, meta={'item': deepcopy(item)})
                    # 发送请求获取下一部分的书的信息
                    next_part_url_temp = 'https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp=1&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAABC&id=IDENTIFYING&cc=571&paging=1&sub=0'
                    ci = item['s_href'].split('-')[1]
                    next_part_url = next_part_url_temp.format(ci)
                    yield scrapy.Request(next_part_url, callback=self.parse_list, meta={'item': deepcopy(item)})

    def parse_list(self, response):
        item = response.meta.get('item')
        # li_list = response.xpath('//div[@id="filter-results"]/ul/li')
        li_list = response.xpath('//li[contains(@class, "book")]')
        for li in li_list:
            item["book_name"] = li.xpath('.//p[@class="sell-point"]/a/text()').extract_first()
            item["book_href"] = li.xpath('.//p[@class="sell-point"]/a/@href').extract_first()
            item["book_store_name"] = li.xpath('.//p[contains(@class, "seller oh no-more")]/a/text()').extract_first()
            yield response.follow(item['book_href'], callback=self.parse_detail, meta={'item': deepcopy(item)})

        # 列表页翻页
        next_url_1 = 'https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp={}&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAABC&id=IDENTIFYING&cc=571'
        next_url_2 = 'https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp={}&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAABC&id=IDENTIFYING&cc=571&paging=1&sub=0'
        ci = item['s_href'].split('-')[1]
        current_page = re.findall('param.currentPage = "(.*?)"', response.text)[0]
        total= re.findall('param.pageNumbers = "(.*?)"', response.text)[0]
        print('cu',current_page)
        print('to',total)
        if int(current_page) < int(total):
            next_page = int(current_page) + 1
            next_url_1 = next_url_1.format(ci, str(next_page))
            yield scrapy.Request(next_url_1, callback=self.parse_list, meta={'item': deepcopy(item)})
            # 构造下一页翻页
            next_url_2 = next_url_2.format(ci, str(next_page))
            yield scrapy.Request(next_url_2,callback=self.parse_list, meta={'item': deepcopy(item)})

    def parse_detail(self, response):
        item = response.meta.get('item')
        p1 = item['book_href'].split('/')[-1].split('.')[0]
        if len(p1) == 9:
            price_temp_price = 'https://pas.suning.com/nspcsale_0_000000000{}_000000000{}_{}_130_571_5710101_502282_1000323_9315_12499_Z001___{}_{}___.html'
        else:
            price_temp_price = 'https://pas.suning.com/nspcsale_0_0000000{}_0000000{}_{}_130_571_5710101_502282_1000323_9315_12499_Z001___{}_{}___.html'
        p2 = p1
        p3 = item['book_href'].split('/')[-2]
        p4 = re.findall('"catenIds":"(.*?)"', response.text)
        if len(p4) > 0:
            p4 = p4[0]
            p5 = re.findall('"weight":"(.*?)"', response.text)[0]
            price_url = price_temp_price.format(p1, p2, p3, p4, p5)
            yield scrapy.Request(price_url, callback=self.get_price, meta={'item':item})

    def get_price(self, response):
        item = response.meta.get('item')
        item['price'] = re.findall('"netPrice":"(.*?)"', response.text)[0]
        print(item)
        yield item



