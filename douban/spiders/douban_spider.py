# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

DOMAIN_URL = 'https://movie.douban.com/top250'


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名
    name = 'douban_spider'
    # 允许爬取的域名
    allowed_domains = ['movie.douban.com']
    # 入口URL
    start_urls = [
        DOMAIN_URL
    ]

    def parse(self, response):
        li_xpath = '//div[@class="article"]//ol[@class="grid_view"]//li'
        movie_list = response.xpath(li_xpath)
        for li in movie_list:
            item = DoubanItem()
            item['serial_number'] = li.xpath('.//div[@class="item"]//em/text()').extract_first()
            item['movie_name'] = li.xpath('.//div[@class="info"]//div[@class="hd"]//a//span/text()').extract_first()
            contents = li.xpath('.//div[@class="info"]//div[@class="bd"]//p[1]/text()').extract()
            for content in contents:
                introduce = "".join(content.split())
            item['introduce'] = introduce
            item['star'] = li.xpath('.//span[@class="rating_num"]/text()').extract_first()
            item['evaluate'] = li.xpath('.//div[@class="star"]//span[4]/text()').extract_first()
            item['describe'] = li.xpath('.//p[@class="quote"]/span/text()').extract_first()
            # yield item to pipelines, 进行数据的清洗或存储
            yield item

        # 解析下一页
        next_link = response.xpath('//span[@class="next"]/link/@href').extract()
        if next_link:
            next_link = next_link[0]
            # 提交至调度器
            yield scrapy.Request(DOMAIN_URL + next_link, callback=self.parse)
