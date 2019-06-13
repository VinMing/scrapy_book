# -*- coding: utf-8 -*-
import scrapy
from properties.items import PropertiesItem
from urllib.parse import urlparse
import datetime
import socket


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    # start_urls = ['http://web:9312/properties/property_000000.html',
    #               'http://web:9312/properties/property_000001.html',
    #               'http://web:9312/properties/property_000002.html']
    start_urls =[i.strip() for i in
                 open('todo.urls.txt').readlines()]


    def parse(self, response):
        # 创建 contract
        """ This function parase a property page.
        @url http://web:3912/properties/property_000000.html
        @returns items L
        @scrapes title price description address image_urls
        @scrapes url project spider server date
        """
        # 比较实用的水平爬取和垂直爬取URL
        # 水平
        urls = response.xpath('//*[contains(@class,"next")]//@href').extract()
        absUrls = [urlparse.urljoin(response.url, i) for i in urls]
        # 垂直
        urls = response.xpath('//*[@itemprop="url"]/@href').extract()
        absUrls = [urlparse.urljoin(response.url, i) for i in urls]
        # 使用爬虫预定义的方法log()，输出在基本字段表中总结的所有内容
        self.log("title: %s" % response.xpath('//*[@itemprop="name"][1]/text()').extract())
        self.log("price: %s" % response.xpath('//*[@itemprop="price"[1]/text()').re('[.0-9]+'))
        self.log("description: %s" % response.xpath('//*[@itemprop="description"][1]/text()').extract())
        self.log("address: %s" % response.xpath('//*[@itemprop="http://schema.org/Place"][1]/text()').extract())
        self.log("image_urls: %s" % response.xpath('//*[@itemprop="image"][1]/@src').extract())

        # # 填充Item
        # item = PropertiesItem()
        # item['title'] = response.xpath('//*[@itemprop="name"][1]/text()').extract()
        # item['price'] = response.xpath('//*[@itemprop="price"[1]/text()').re('[.0-9]+')
        # item['description'] = response.xpath('//*[@itemprop="description"][1]/text()').extract()
        # item['address'] = response.xpath('//*[@itemprop="http://schema.org/Place"][1]/text()').extract()
        # item['image_urls'] = response.xpath('//*[@itemprop="image"][1]/@src').extract()
        # return item


        # 清理 item 装载器与管理字段
        L = ItemLoader(item=PropertiesItem(), response=response)
        L.add_xpath('title', '//*[@itemprop="name"][1]/text()')
        L.add_xpath('price', '//*[@itemprop="price"][1]/text()', re='[.0-9]+')
        L.add_xpath('description', '//*[@itemprop="description"][1]/text()')
        L.add_xpath('address', '//*[@itemprop="http://schema.org/Place"][1]/text()')
        L.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src')


        # 使用处理器 用来对我们的Xpath/CSS结果进行处理。
        # 在爬虫中使用几个这样子的处理器，并按照我们想要的方式输出
        L.add_xpath('title', '//*[@itemprop="name"][1]/text()', MapCompose(unicode.strip, unicode.title))
        L.add_xpath('price', '//*[@itemprop="price"][1]/text()', MapCompose(lambda i: i.replace(',', ''), float), re='[.0-9]+')
        L.add_xpath('description', '//*[@itemprop="description"][1]/text()', MapCompose(unicode.strip), Join())
        L.add_xpath('address', '//*[@itemprop="http://schema.org/Place"][1]/text()', MapCompose(unicode.strip))
        L.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src', MapCompose(lambda i : urlparse.urljoin(response.url, i)))

        # 使用add_value方法设置管理字段
        L.add_value('url', reponse.url)
        L.add_value('project', self.settings.get('BOT_NAME'))
        L.add_value('spider', self.name)
        L.add_value('server', socket.gethostname)
        L.add_value('date', datetime.datetime.now())
        return L.load_item()
        pass
