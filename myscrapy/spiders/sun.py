# -*- coding: utf-8 -*-
import scrapy

from myscrapy.items import MyscrapyItem


class SunSpider(scrapy.Spider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

    def parse(self, response):
        tr_list = response.xpath('//div[@class="greyframe"]/table[2]/tr/td/table/tr')
        for tr in tr_list:
            item = MyscrapyItem()
            item['num'] = tr.xpath('./td[1]/text()').extract_first()
            item['title'] = tr.xpath('./td[2]/a[2]/text()').extract_first()
            item['href'] = tr.xpath('./td[2]/a[2]/@href').extract_first()
            item['status'] = tr.xpath('./td[3]/span/text()').extract_first()
            item['name'] = tr.xpath('./td[4]/text()').extract_first()
            item['publish_date'] = tr.xpath('./td[5]/text()').extract_first()
            yield scrapy.Request(item['href'],callback=self.parse_detail, meta={'item':item})
        #构造下一页请求,翻页
        next_url = response.xpath('//a[text()=">"]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta.get('item')
        item['img'] = response.xpath('//div[@class="textpic"]/img/@src').extract_first()
        item['content'] = response.xpath('//td[@class="txt16_3"]/text()').extract()
        yield item

