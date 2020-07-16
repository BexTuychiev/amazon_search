# -*- coding: utf-8 -*-
import scrapy
import logging


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['amazon.com']

    def start_requests(self):
        yield scrapy.Request(url=f'https://www.amazon.com/s?k={self.query}')

    def parse(self, response):
        result_divs = response.xpath("//div[@data-component-type='s-search-result']")
        for div in result_divs:
            # Retrieve product information
            product_name = div.xpath(
                "normalize-space(.//span[@class='a-size-base-plus a-color-base a-text-normal']/text())").get()
            product_price = div.xpath("normalize-space(.//span[@class='a-price-whole']/text())").get()
            product_details_page = 'https://www.amazon.com' + div.xpath(
                ".//a[@class='a-link-normal a-text-normal']/@href").get()
            image = div.xpath(".//img[@data-image-latency='s-product-image']/@src").get()
            rating = div.xpath("normalize-space(.//span[@class='a-icon-alt']/text())").get()

            yield {'product_name': product_name,
                   'product_price': product_price,
                   'product_details_page': product_details_page,
                   'image_url': image,
                   'rating': rating}

        # Check for the next page
        next_page = 'https://www.amazon.com' + response.xpath("//li[@class='a-last']/a/@href").get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)
