import scrapy

from scrapy.shell import inspect_response
from scrapy.loader import ItemLoader

from pricesmart.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["www.pricesmart.com"]

    def start_requests(self):
        url = "https://www.pricesmart.com/site/sv/en/pdp/"
        item_number = getattr(self, "item_number", None)
        if item_number:
            url += item_number
            yield scrapy.Request(
                url=url,
                callback=self.parse,
            )

    def parse(self, response):
        # inspect_response(response, self)
        pi = ItemLoader(item=ProductItem())
        pi.add_value("brand_name", response.css(".brand-exclusive::text").get())
        pi.add_value("brand_img", response.css(".brand-logo img::attr(src)").get())
        pi.add_value("item_number", response.css("#itemNumber::text").get())
        pi.add_value("title", response.css("#product-display-name::text").get())
        pi.add_value("price", response.css("#product-price::text").get())
        pi.add_value(
            "clubs",
            response.css(
                "#clubs-selection div div:nth-child(3) span.product-container-inner::text"
            ).getall(),
        )
        pi.add_value(
            "delivery_methods",
            response.css(
                "span.pdp-delivery-availability-title ~ ul li span::text"
            ).getall(),
        )
        pi.add_value(
            "description",
            response.css(
                "#product-description span.product-container-inner::text"
            ).get(),
        )
        pi.add_value(
            "images", response.css(".product-thumb-cont img::attr(src)").getall()
        )
        pi.add_value("product_info", response.css("#collapseOne .card-body").get())

        yield pi.load_item()
