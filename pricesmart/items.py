# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


def is_instore(value):
    return bool(value)


def filter_information(value):
    """
    Takes the raw text in the product information, cleans it,
    and returns the information text without the item number.
    Items that don't have information return an empty string.
    """
    lines = [l.strip() for l in value.split("\n")]
    # remove empty values
    lines = list(filter(len, lines))
    # the first line is always the item number, so skip it if
    # there is more than one line
    if len(lines) > 1:
        return lines[1]

    return ""


class ProductItem(scrapy.Item):
    brand_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    brand_img = scrapy.Field(
        output_processor=TakeFirst(),
    )
    item_number = scrapy.Field(
        output_processor=TakeFirst(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    in_stock = scrapy.Field(
        input_processor=MapCompose(is_instore),
        output_processor=TakeFirst(),
    )
    clubs = scrapy.Field()
    delivery_methods = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    images = scrapy.Field()
    product_info = scrapy.Field(
        input_processor=MapCompose(remove_tags, filter_information),
        output_processor=TakeFirst(),
    )


def parse_category_id(value):
    return value.split("?cat=")[-1]


def parse_name(value):
    return value.split("/")[-1].split("?cat=")[0]


class CategoryItem(scrapy.Item):
    """
    Represents a category or subcategory.
    Categories of the type 'main' have subcategories.
    """

    MAIN_CATEGORY = "main_category"
    SUBCATEGORY = "subcategory"
    CATEGORY_TYPES = (
        (MAIN_CATEGORY, "Main category"),
        (SUBCATEGORY, "Subcategory"),
    )

    name = scrapy.Field(
        input_processor=MapCompose(parse_name), output_processor=TakeFirst()
    )
    verbose_name = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    )
    id = scrapy.Field(
        input_processor=MapCompose(parse_category_id), output_processor=TakeFirst()
    )
    type = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    subcategories = scrapy.Field()
