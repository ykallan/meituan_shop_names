# -*- coding: utf-8 -*-
import scrapy
import re
import math
from ..items import MeituanItem


class MtSpider(scrapy.Spider):
    name = 'mt'
    # allowed_domains = ['meituan.com']
    start_urls = ['https://www.meituan.com/changecity/']
    base_https = 'https:'
    meishi_url = 'https://www.meituan.com/meishi/{}/'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        city_urls = response.xpath('//span[@class="cities"]/a/@href').getall()
        for city in city_urls:
            yield scrapy.Request(url=self.base_https+city,callback=self.parse_citys)

    def parse_citys(self, response):
        next_parse_city_meishi = response.xpath(
            '//span[@class="nav-text-wrapper"][1]/span/a[@data-bid="b_atx2p7dc"]/@href').get()
        yield scrapy.Request(url=next_parse_city_meishi, callback=self.city)

    def city(self, response):
        shop_ids = re.findall(r'"poiId":(\d*),"frontImg', response.text, re.S)
        total_num = re.findall(r'totalCounts":(\d*),"', response.text)[0]

        for shop_id in shop_ids:
            yield scrapy.Request(url=self.meishi_url.format(shop_id), callback=self.parse_detail)

        pages = int(math.floor(int(total_num)/15.)+1)
        if pages > 1:
            for i in range(2, pages):
                if 'pn' in response.url:
                    yield scrapy.Request(url=response.url.split('pn')[0]+'pn{}/'.format(i), callback=self.city)
                else:
                    yield scrapy.Request(url=response.url+'pn{}/'.format(i), callback=self.city)

    def parse_detail(self, response):
        typer = re.findall(r'\{"title":"(.*?)","url"', response.text, re.S)[0].replace('美团', '')  # 地区
        name = re.findall(r'poiId":\d*,"name":"(.*?)","', response.text, re.S)[0]
        avgScore = re.findall(r'avgScore":(.*?),"a', response.text, re.S)[0]
        address = re.findall(r'address":"(.*?)","', response.text, re.S)[0]
        phone = re.findall(r'phone":"(.*?)","', response.text, re.S)[0]
        openTime = re.findall(r'openTime":"(.*?)","', response.text, re.S)[0]

        item = MeituanItem()
        item['typer'] = typer
        item['name'] = name
        item['avgScore'] = avgScore
        item['address'] = address
        item['phone'] = phone
        item['openTime'] = openTime

        yield item
