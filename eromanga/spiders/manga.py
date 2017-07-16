# -*- coding: utf-8 -*-
import scrapy
import re
from eromanga.items import EromangaItem
from inline_requests import inline_requests
from scrapy import Request

class MangaSpider(scrapy.Spider):
    name = 'manga'
    allowed_domains = ['177pic.info']
    item = EromangaItem()

    def start_requests(self):
        base_url = 'http://www.177pic.info/html/category/tt'
        yield Request(url=base_url, callback=self.parse)

    @inline_requests
    def parse(self, response):
        titles = []
        urls = []
        pages = []
        lastpage = int(response.xpath('//div[@class="wp-pagenavi"]//a[@class="last"]/@href').extract_first().split('/')[-1])
        startpage = 1
        # lastpage = 6
        for i in range(startpage, lastpage+1):
            r = yield Request(url=response.url + '/page/' + str(i))
            titles.extend(r.xpath('//h2[@class="h1"]//a/text()').extract())
            urls.extend(r.xpath('//h2[@class="h1"]//a//@href').extract())
        for title, url in zip(titles, urls):
            res = yield Request(url=url)
            pageurls = [url]
            pageurls += res.xpath('//*[@id="single-navi"]/div/p/a[span]/@href').extract()
            for pageurl in pageurls:
                res = yield Request(url=pageurl, dont_filter=True)
                if ('manga' in self.item):
                    self.item['manga'] += res.xpath('//img/@src').extract()
                else:
                    self.item['manga'] = res.xpath('//img/@src').extract()
            self.item['title'] = title
            self.item['url'] = url
            yield self.item
