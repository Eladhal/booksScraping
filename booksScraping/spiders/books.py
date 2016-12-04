# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ['books.toscrape.com']
    start_urls = (
        'http://books.toscrape.com',
    )

    def parse(self, response):
        books = response.xpath('//*[@class="product_pod"]')
        for book in books:
            link = book.xpath('.//*[@class="image_container"]/a/@href').extract_first()
            absolute_url = response.urljoin(link)
            yield Request(absolute_url,callback = self.detailedParsed)
        nextUrl = response.xpath('.//*[@class="next"]/a/@href').extract_first()
        fullNextUrl = response.urljoin(nextUrl)
        yield Request(fullNextUrl,callback = self.parse)


    def detailedParsed(self,response):
        catalog = response.xpath('.//*[@class="breadcrumb"]/li[3]/a/text()').extract_first()
        description = response.xpath('.//*[@class="product_page"]/p/text()').extract_first()
        name = response.xpath('.//*[@class="col-sm-6 product_main"]/h1/text()').extract_first()
        price = response.xpath('.//*[@class="col-sm-6 product_main"]/p[1]/text()').extract_first()
        rating = response.xpath('.//*[@class="col-sm-6 product_main"]/p[3]/@class').extract_first()
        string = response.xpath('.//*[@class="instock availability"]/text()').extract()
        availability = string[1].split()[0]+' '+string[1].split()[1]
        yield {"Name":name,"Rating":rating,"Price":price,"Availiabilty":availability,"Description":description,"Catalog":catalog}




