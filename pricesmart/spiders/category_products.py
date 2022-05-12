import scrapy

from scrapy.loader import ItemLoader

from pricesmart.items import ProductItem


class CategoryProductsSpider(scrapy.Spider):
    name = "category_products"
    allowed_domains = ["www.pricesmart.com"]

    def start_requests(self):
        self.product_url = "https://www.pricesmart.com/site/sv/en/pdp/"
        url = "https://www.pricesmart.com/site/sv/en/category/"
        category = getattr(self, "category")
        url += category
        yield scrapy.Request(
            url=url,
            callback=self.parse_category,
            cb_kwargs={"category": category},
        )

    def parse_category(self, response, category):
        products = []

        product_links = response.css(".search-product-box a::attr(href)").getall()
        for pl in product_links:
            product_id = pl.split("/")[-1]
            products.append(product_id)
            yield scrapy.Request(
                url=self.product_url + product_id, callback=self.parse_product
            )

        next_page = response.css("li#next a::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_category,
                cb_kwargs={"category": category},
            )

    def parse_product(self, response):
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
