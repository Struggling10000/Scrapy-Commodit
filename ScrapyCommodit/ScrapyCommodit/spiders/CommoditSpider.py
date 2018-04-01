# -*- coding: utf-8 -*-
import logging
import random
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

from ScrapyCommodit.items import ScrapycommoditItem

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class CommoditspiderSpider(scrapy.Spider):
    name = 'CommoditSpider'
    allowed_domains = ['jd.com']
    start_urls = [
        'http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10001-1#comfort']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):
        log = self.logger
        try:
            lis = response.xpath('/html/body/div[8]/div[2]/div[3]/div/ul/li')

            for li in lis:
                # print(li.extract())
                item = ScrapycommoditItem()

                # random.seed()
                # item["itemId"] = int(random.random()*100000000000000)

                img = li.xpath(
                    'div[2]/a/img/@data-lazy-img').extract()[0].replace("\r\n", "").strip()
                if img == 'done':
                    img = li.xpath(
                    'div[2]/a/img/@src').extract()[0].replace("\r\n", "").strip()
                item['itemImg'] = urljoin(response.url, img)

                item['itemTitle'] = li.xpath(
                    'div[3]/a/text()').extract()[0].replace("\r\n", "").strip()

                item['itemPrice'] = li.xpath(
                    'div[3]/dl[4]/dd/em/text()').extract()[0].replace("\r\n", "").strip()
                yield item
        except Exception as e:
            log.error(e)
        try:
            nextPage = response.xpath(
                '/html/body/div[8]/div[2]/div[4]/div/div/span/a[7]/@href').extract()[0]
            nextPage = urljoin(response.url, nextPage)
            yield SplashRequest(nextPage, callback=self.parse,args={'wait': 1})
        except Exception as e:
            log.error(e)
