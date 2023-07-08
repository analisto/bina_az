import scrapy
import re

class PropertySpider(scrapy.Spider):
    name = "property_spider"
    start_urls = ["https://bina.az/alqi-satqi?page=1"]

    def parse(self, response):
        items = response.css("div.items-i")

        for item in items:
            link = item.css("a::attr(href)").get()
            absolute_link = response.urljoin(link)
            yield scrapy.Request(absolute_link, callback=self.parse_property)

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_property(self, response):
        def extract_text(selector):
            return selector.css("::text").get().strip() if selector else None

        def extract_phone_number(selector):
            phone_number = selector.css("a::attr(href)").get()
            return re.sub(r'\D', '', phone_number) if phone_number else None

        data = {
            'url': response.url,
            'phone number': extract_phone_number(response.css("div.product-phones__list-i")),
            'owner name': extract_text(response.css("div.product-owner__info-name")),
            'owner category': extract_text(response.css("div.product-owner__info-region")),
            'category': extract_text(response.css("div.product-properties__i span.product-properties__i-value")),
            'floor': extract_text(response.css("div.product-properties__i:nth-child(3) span.product-properties__i-value")),
            'area': extract_text(response.css("div.product-properties__i:nth-child(4) span.product-properties__i-value")),
            'room count': extract_text(response.css("div.product-properties__i:nth-child(5) span.product-properties__i-value")),
            'description': extract_text(response.css("div.product-properties__i:nth-child(6) span.product-properties__i-value")),
            'mortgage': extract_text(response.css("div.product-properties__i:nth-child(7) span.product-properties__i-value")),
            'price': re.sub(r'\s+', '', extract_text(response.css("div.product-price__i.product-price__i--bold span.price-val"))),
            'currency': extract_text(response.css("div.product-price__i.product-price__i--bold span.price-cur"))
        }

        yield data
