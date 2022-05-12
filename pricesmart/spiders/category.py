import scrapy

from scrapy.loader import ItemLoader
from scrapy.shell import inspect_response

from pricesmart.items import CategoryItem


class CategorySpider(scrapy.Spider):
    name = "category"
    allowed_domains = ["www.pricesmart.com"]
    start_urls = ["http://www.pricesmart.com/"]

    def parse(self, response):
        # inspect_response(response, self)
        categories = response.css("#categories-section div a")

        for cat in categories:
            ci = ItemLoader(item=CategoryItem())
            ci.add_value("name", cat.css("a::attr(href)").get())
            ci.add_value("verbose_name", cat.css("div::text").get())
            ci.add_value("id", cat.css("a::attr(href)").get())
            ci.add_value("url", cat.css("a::attr(href)").get())
            ci.add_value("type", CategoryItem.MAIN_CATEGORY)

            # preload to access cleaned name
            category = ci.load_item()
            # load subcategories for the given category
            html_id = cat.css("div::attr(id)").get()
            subcategories = response.xpath(f"//div[@data-category='{html_id}']//a")
            for scat in subcategories:
                sci = ItemLoader(item=CategoryItem())
                sci.add_value("name", scat.css("a::attr(href)").get())
                sci.add_value("verbose_name", scat.css(".subcategory::text").get())
                sci.add_value("id", scat.css("a::attr(href)").get())
                sci.add_value("url", scat.css("a::attr(href)").get())
                sci.add_value("type", CategoryItem.SUBCATEGORY)
                ci.add_value("subcategories", sci.load_item())

            yield ci.load_item()
