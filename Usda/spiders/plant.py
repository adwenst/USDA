# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request
import logging
import urlparse


class PlantSpider(CrawlSpider):
    name = 'plant'
    allowed_domains = ['plants.usda.gov']
    start_urls = ['https://plants.usda.gov/java/factSheet']

    # 制定获取链接的规则
    rules = (
        # pdf链接获取不到，(可能是需要什么处理)，采取折中的方法，xpath匹配获取并发起请求
        # Rule(LinkExtractor(allow=r'/pdf/'), callback='parse_pdf', follow=False),
        Rule(LinkExtractor(allow=r'profile\?symbol=', ), callback='parse_profile', follow=True),
        Rule(LinkExtractor(allow=r'/java/charProfile\?symbol=', ), callback='parse_char', follow=False),
    )

    # 解析初始页面
    def parse_start_url(self, response):
        # get key from start_url
        logging.debug("parsing start page...")
        key = response.xpath('//th[@align="left" and @scope="col"]/a/text()').extract()
        key = [k.replace(' ', '_') for k in key]
        logging.debug(msg="field_lst is [%s]" % ','.join(key))

        # get key-value
        plants = list()
        value_nodes = response.xpath('//tr[@class="rowon"]')
        for node in value_nodes:
            plant = dict()
            # Symbol
            plant[key[0]] = node.xpath('th/text()').extract()[0].replace(' ', '_')
            # Scientific Name
            plant[key[1]] = node.xpath('td[1]').xpath('string(.)').extract()[0].replace(' ', '_')
            # Common Name(part is none)
            try:
                plant[key[2]] = node.xpath('td[2]/text()').extract()[0].replace(' ', '_')
            except IndexError:
                plant[key[2]] = ''
            # get pdf url and send request
            pdf_base = r'https://plants.usda.gov'
            pdf_links = node.xpath('.//a[contains(@title,"pdf")]/@href').extract()

            for link in pdf_links:
                yield Request(url=urlparse.urljoin(base=pdf_base, url=link), callback=self.parse_pdf)
            plants.append(plant)
        logging.debug(msg="get %d plants' attribute:%s" % (len(plants), '|'.join(key[0:3])))
        yield plants

    # 解析pdf文件
    def parse_pdf(self, response):
        logging.debug("parsing pdf...")
        # pdf_type（pg或者fs）表示pdf文件是	Fact Sheets还是Plant Guides，
        # 需要添加到从pdf中得到的字段前面去
        pdf_type, symbol = response.url.split('/')[-1].split('.')[0].split('_')
        # 作为测试将写pdf写入本地，实际可以直接处理
        # response.body即是pdf
        with open('Data/%s.txt' % symbol, 'wb')as f:
            f.write(response.body)
        pdf_dict = self.get_dict_from_pdf(response.body)
        return pdf_dict

    # 获取pdf中的键值对（段名：正文）
    def get_dict_from_pdf(self, pdf):
        pdf_dict = dict()
        # 具体操作，将pdf文件中的键值对保存到pdf_dict中
        return pdf_dict

    # parse profile pages
    def parse_profile(self, response):
        logging.debug(msg="parsing profile page...")
        info_nodes = response.xpath('//div[@id="tabGeneral"]/div[1][@class="left"]/table[@class="bordered"]/tr')
        info_dict = dict()
        # 只获取一部分属性
        for node in info_nodes[1:7]:
            key = '_'.join(node.xpath('td[1]').xpath('string(.)').re(r'[a-zA-Z]+'))
            try:
                value = ' '.join(node.xpath('td[2]').xpath('string(.)').re(r'[a-zA-Z\d]+'))
            except IndexError:
                value = ''
            info_dict[key] = value
        print info_dict, '\n', response.url
        return info_dict

    # parse characteristic pages
    def parse_char(self, response):
        logging.debug(msg="start parsing characteristic...")
        char_nodes = response.xpath('//table[@cellpadding="3"]/tr[not(@align)]')
        char_dict = dict()
        for node in char_nodes:
            key = node.xpath('td[1]/text()').extract()[0].replace(' ', '_')
            try:
                value = node.xpath('td[2]/text()').extract()[0].strip()
            except IndexError:
                value = ''
            char_dict[key] = value
        return char_dict
