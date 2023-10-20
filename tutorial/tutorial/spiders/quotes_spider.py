from pathlib import Path
from typing import Any, Iterable

import scrapy
from scrapy.http import Request, Response

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
    
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = Response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)